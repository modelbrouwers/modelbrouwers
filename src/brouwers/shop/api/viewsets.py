from rest_framework import viewsets

from ..models import Cart, CartProduct, Product
from .serializers import (
    CartProductSerializer, CartSerializer, ProductSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        qs = super(CartViewSet, self).get_queryset()
        if self.request.user:
            qs = Cart.objects.filter(user=self.request.user)
        return qs


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def get_queryset(self):
        qs = super(CartProductViewSet, self).get_queryset()
        if self.request.user:
            qs = CartProduct.objects.filter(cart__user=self.request.user)
        return qs
