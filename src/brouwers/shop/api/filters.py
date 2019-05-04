import rest_framework_filters as filters

from brouwers.users.api.filters import UserFilter
from brouwers.users.models import User

from ..models import Cart, CartProduct, Product


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'price', 'vat')


class CartFilter(filters.FilterSet):
    user = filters.RelatedFilter(UserFilter, queryset=User.objects.all())

    class Meta:
        model = Cart
        fields = ('id', 'user', 'status')


class CartProductFilter(filters.FilterSet):
    cart = filters.RelatedFilter(CartFilter, queryset=Cart.objects.all())
    product = filters.RelatedFilter(ProductFilter, queryset=Product.objects.all())

    class Meta:
        model = CartProduct
        fields = ('id', 'product', 'cart', 'amount')
