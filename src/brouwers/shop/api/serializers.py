from collections import OrderedDict

from rest_framework import serializers

from brouwers.users.api.serializers import UserSerializer

from ..models import Cart, CartProduct, PaymentMethod, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "brand",
            "image",
            "price",
            "vat",
            "categories",
            "model_name",
        )


class ProductField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        pk = super().to_representation(value)
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
        fields = ("id", "product", "amount", "cart", "total")


class WriteCartProductSerializer(serializers.ModelSerializer):
    product = ProductField(queryset=Product.objects.all())

    class Meta:
        model = CartProduct
        fields = ("id", "product", "amount", "cart", "total")

    def validate_cart(self, value):
        cart = value
        request = self.context["request"]
        qs = Cart.objects.for_request(request)

        if not qs.filter(id=cart.id).exists():
            raise serializers.ValidationError({"cart": "invalid cart"})
        return value

    def create(self, validated_data):
        """
        Increase cart product amount if product is already in the cart. Otherwise add product to cart
        """
        cart = Cart.objects.get(id=validated_data["cart"].id)
        qs = cart.products.filter(product=validated_data["product"])
        if qs:
            cp = qs.get()
            cp.amount += validated_data["amount"]
            cp.save()
            return cp
        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    total = serializers.SerializerMethodField()
    products = ReadCartProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("id", "user", "status", "products", "total")

    def get_total(self, obj):
        return obj.total


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ("id", "name", "logo", "order")
