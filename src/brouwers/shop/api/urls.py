from django.urls import path

from .views import CartView, IdealBanksView

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart-detail"),
    path("ideal_banks/", IdealBanksView.as_view(), name="ideal-banks"),
]
