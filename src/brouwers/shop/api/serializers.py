from collections import OrderedDict
from django.db.models import Q

from rest_framework import serializers

from brouwers.users.api.serializers import UserSerializer

from ..models import Cart, CartProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'image', 'price', 'vat', 'categories')


class ProductField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        pk = super(ProductField, self).to_representation(value)
        try:
            item = Product.objects.get(pk=pk)
            serializer = ProductSerializer(item)
            return serializer.data
        except Product.DoesNotExist:
            return None

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        return OrderedDict([(item.id, str(item)) for item in queryset])


class ReadCartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = ('id', 'product', 'amount', 'cart', 'total')


class WriteCartProductSerializer(serializers.ModelSerializer):
    product = ProductField(queryset=Product.objects.all())

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


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    total = serializers.SerializerMethodField()
    products = ReadCartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'status', 'products', 'total')

    def get_total(self, obj):
        return obj.total
