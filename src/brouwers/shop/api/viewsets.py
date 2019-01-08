from rest_framework import viewsets, views, generics
from rest_framework.response import Response

from ..models import Cart, CartProduct, Product
from .serializers import (
    CartProductSerializer, CartSerializer, ProductSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(views.APIView):
    def get(self, request, *args, **kwargs):
        cart_id = None

        if request.session.get('cart_id'):
            cart_id = request.session['cart_id']
        elif hasattr(request.user, 'carts'):
            cart_id = request.user.carts.last().id

        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            if request.user.is_authenticated():
                cart = Cart.objects.create(user=request.user)
            else:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id

        response = {'cart': CartSerializer(cart).data}
        return Response(response)


class CartProductViewSet(viewsets.ModelViewSet):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def get_queryset(self):
        qs = super(CartProductViewSet, self).get_queryset()
        if self.request.user:
            qs = CartProduct.objects.filter(cart__user=self.request.user)
        return qs
