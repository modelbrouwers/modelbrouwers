from django.urls import path

from .viewsets import CartViewSet, IdealBanksViewSet

urlpatterns = [
    path("cart/", CartViewSet.as_view(), name="cart-detail"),
    path('ideal_banks/', IdealBanksViewSet.as_view(), name='ideal-banks'),
]
