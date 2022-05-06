from django.urls import path

from .views import IdealBanksView
from .viewsets import CartViewSet

urlpatterns = [
    path("cart/", CartViewSet.as_view(), name="cart-detail"),
    path("ideal_banks/", IdealBanksView.as_view(), name="ideal-banks"),
]
