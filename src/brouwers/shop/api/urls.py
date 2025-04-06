from django.urls import path

from .views import CartView, GetShippingCostsView, IdealBanksView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("ideal_banks/", IdealBanksView.as_view(), name="ideal-banks"),
    path("shipping-costs/", GetShippingCostsView.as_view(), name="shipping-costs"),
]
