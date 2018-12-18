from django.core.urlresolvers import reverse

from rest_framework import fields, serializers

from brouwers.users.api.serializers import UserSerializer

from ..models import Cart, CartProduct, Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'image', 'price', 'vat', 'categories')


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'status', 'cart_products')


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ('id', 'product', 'amount')
