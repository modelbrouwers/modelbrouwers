from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from ..models import Order


class BackofficeRequiredMixin(PermissionRequiredMixin):
    permission_required = "shop.can_change_order"


class OrderListView(BackofficeRequiredMixin, ListView):
    queryset = Order.objects.select_related("cart", "payment").order_by("-created")
    context_object_name = "orders"
    template_name = "shop/backoffice/order_list.html"
    paginate_by = 25
