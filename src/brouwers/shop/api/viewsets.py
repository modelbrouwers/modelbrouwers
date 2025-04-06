from rest_framework import viewsets

from ..models import Cart, CartProduct, PaymentMethod, Product
from .filters import CartProductFilter
from .serializers import (
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
        valid_carts = Cart.objects.for_request(self.request)
        return qs.filter(cart__in=valid_carts)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadCartProductSerializer
        else:
            return WriteCartProductSerializer


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentMethod.objects.filter(enabled=True).order_by("order", "name")
    pagination_class = None
    serializer_class = PaymentMethodSerializer
