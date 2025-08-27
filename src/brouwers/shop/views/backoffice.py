from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, TemplateView, UpdateView

from ..constants import OrderStatuses
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
    queryset = Order.objects.select_related("cart", "payment")
    form_class = OrderDetailForm
    slug_field = "reference"
    slug_url_kwarg = "reference"
    template_name = "shop/backoffice/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_products"] = sum(
            cart_product.amount for cart_product in context["order"].cart.products.all()
        )
        return context

    def get_success_url(self) -> str:
        return reverse("shop:order-detail", kwargs={"reference": self.object.reference})
