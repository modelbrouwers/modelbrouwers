from django.urls import path

from .viewsets import CartViewSet

urlpatterns = [
    path("cart/", CartViewSet.as_view(), name="cart-detail"),
]
