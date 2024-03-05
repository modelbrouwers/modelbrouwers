from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView

from ..constants import OrderStatuses
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
    paginate_by = 25


class OrderDetailView(BackofficeRequiredMixin, DetailView):
    queryset = Order.objects.select_related("cart", "payment")
    slug_field = "reference"
    slug_url_kwarg = "reference"
    template_name = "shop/backoffice/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_products"] = sum(
            (
                cart_product.amount
                for cart_product in context["order"].cart.products.all()
            )
        )
        return context
