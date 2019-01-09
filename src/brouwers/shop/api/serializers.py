from django.db.models import Q
from rest_framework import serializers

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

    def create(self, validated_data):
        cart, created = Cart.objects.get_or_create(
            id=self.request.session.cart_id,
            user=self.request.user)
        if not self.request.session.cart_id:
            self.request.session.cart_id = cart.id
        return cart


class ReadCartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    cart = CartSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ('id', 'product', 'amount', 'cart')


class WriteCartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('id', 'product', 'amount', 'cart')

    def validate_cart(self, value):
        cart = value
        request = self._context['request']
        qs = Cart.objects.filter(Q(user=request.user) | Q(id=request.session.get('cart_id')))

        if cart not in qs:
            raise serializers.ValidationError({"cart": "invalid cart"})
        return value
