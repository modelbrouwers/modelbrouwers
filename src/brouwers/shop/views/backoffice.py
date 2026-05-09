from functools import partial

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models, transaction
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, TemplateView, UpdateView

from privates.views import PrivateMediaView

from brouwers.shop.models.cart import CartProduct

from ..constants import DeliveryMethods, OrderEvents, OrderStatuses
from ..emails import send_order_update_email
from ..forms import OrderDetailForm
from ..models import Order
from ..sendcloud import Client as SendcloudClient


class BackofficeRequiredMixin(PermissionRequiredMixin):
    permission_required = "shop.change_order"


class DashboardView(BackofficeRequiredMixin, TemplateView):
    template_name = "shop/backoffice/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "new_order_count": Order.objects.filter(
                    status=OrderStatuses.received
                ).count(),
            }
        )
        return context


class OrderListView(BackofficeRequiredMixin, ListView):
    queryset = Order.objects.select_related("cart", "payment").order_by("-created")
    context_object_name = "orders"
    template_name = "shop/backoffice/order_list.html"
    paginate_by = 20


class OrderDetailView(BackofficeRequiredMixin, UpdateView):
    queryset = Order.objects.select_related(
        "cart", "payment", "delivery_address", "invoice_address"
    ).prefetch_related(
        models.Prefetch(
            "cart__products", queryset=CartProduct.objects.select_related("product")
        )
    )
    form_class = OrderDetailForm
    slug_field = "reference"
    slug_url_kwarg = "reference"
    template_name = "shop/backoffice/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "DeliveryMethods": DeliveryMethods,
                "num_products": sum(
                    cart_product.amount
                    for cart_product in context["order"].cart.products.all()
                ),
                "OrderEvents": OrderEvents,
                "history": context["order"].orderevent_set.order_by("-timestamp"),
            }
        )
        return context

    @transaction.atomic()
    def form_valid(self, form):
        # fetch old record from DB so that no mutation can affect old vs new state
        # comparison
        old_state = self.get_object()

        response = super().form_valid(form)

        order = self.object
        changed_fields = Order.get_changed_fields(old_state, order)
        if "payment.status" in changed_fields:
            order.orderevent_set.create(
                event=OrderEvents.payment_status_changed,
                event_data={
                    "old": old_state.payment.status,
                    "new": order.payment.status,
                },
            )
        if "status" in changed_fields:
            order.orderevent_set.create(
                event=OrderEvents.status_changed,
                event_data={
                    "old": old_state.status,
                    "new": order.status,
                },
            )

        if form.cleaned_data.get("send_email_notification") and changed_fields:
            base_url = self.request.build_absolute_uri(reverse("index"))
            transaction.on_commit(
                partial(
                    send_order_update_email,
                    order=order,
                    base_url=base_url,
                    changed_fields=changed_fields,
                )
            )

        return response

    def get_success_url(self) -> str:
        return reverse("shop:order-detail", kwargs={"reference": self.object.reference})


class OrderShippingLabelView(BackofficeRequiredMixin, PrivateMediaView):
    queryset = Order.objects.filter(
        delivery_method=DeliveryMethods.mail
    ).select_related("delivery_address", "cart")
    slug_field = "reference"
    slug_url_kwarg = "reference"
    file_field = "shipping_label"

    def has_permission(self):
        has_base_perms = super().has_permission()
        if not has_base_perms:
            return False

        has_shipping_label = bool(self.get_object().shipping_label)
        match self.request.method:
            case "POST":
                return not has_shipping_label
            case "GET":
                return has_shipping_label

        return False

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """
        Create a shipping label through Sendcloud.
        """
        order: Order = self.get_object()
        response = HttpResponseRedirect(
            reverse("shop:order-detail", kwargs={"reference": order.reference})
        )

        with SendcloudClient() as client:
            if not client.is_ready_for_use:
                messages.warning(request, _("Sendcloud is not (yet) configured."))
                return response

            result = client.create_shipping_label(
                customer_name=" ".join([order.first_name, order.last_name]).strip(),
                street=order.delivery_address.street,
                number=order.delivery_address.number,
                postal_code=order.delivery_address.postal_code,
                city=order.delivery_address.city,
                country=order.delivery_address.country,
                company=order.delivery_address.company,
                weight_in_grams=order.cart.weight,
            )
            order.sendcloud_shipment_id = result.id
            order.track_and_trace_code = result.tracking_number
            order.track_and_trace_link = result.tracking_url
            order.shipping_label.save(
                name=f"sendcloud-label-{order.reference}{result.label_ext}",
                content=result.label_file,
                save=False,
            )
            order.save()
            messages.success(request, _("Label created."))

        return response
