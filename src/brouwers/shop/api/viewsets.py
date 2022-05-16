from rest_framework import views, viewsets
from rest_framework.response import Response

from ..models import Cart, CartProduct, PaymentMethod, Product
from .filters import CartProductFilter
from .serializers import (
    CartSerializer,
    PaymentMethodSerializer,
    ProductSerializer,
    ReadCartProductSerializer,
    WriteCartProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    filterset_class = CartProductFilter
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = CartProduct.objects.filter(cart__user=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadCartProductSerializer
        else:
            return WriteCartProductSerializer


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.filter(enabled=True).order_by("order", "name")
    pagination_class = None
    serializer_class = PaymentMethodSerializer
