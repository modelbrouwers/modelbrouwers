from .backoffice import DashboardView, OrderDetailView, OrderListView
from .dev import OrderConfirmationEmailView
from .public import (
    CartDetailView,
    CategoryDetailView,
    CheckoutView,
    ConfirmOrderView,
    IndexView,
    ProductDetailView,
    RouterView,
)

__all__ = [
    "IndexView",
    "RouterView",
    "CategoryDetailView",
    "ProductDetailView",
    "CartDetailView",
    "CheckoutView",
    "ConfirmOrderView",
    "OrderConfirmationEmailView",
    # backoffice
    "DashboardView",
    "OrderListView",
    "OrderDetailView",
]
