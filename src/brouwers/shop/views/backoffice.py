from functools import partial

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models, transaction
from django.urls import reverse
from django.views.generic import ListView, TemplateView, UpdateView

from brouwers.shop.models.cart import CartProduct

from ..constants import DeliveryMethods, OrderEvents, OrderStatuses
from ..emails import send_order_update_email
from ..forms import OrderDetailForm
from ..models import Order


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
