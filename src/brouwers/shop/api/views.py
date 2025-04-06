from django.utils.formats import number_format

from rest_framework import serializers, views
from rest_framework.request import Request
from rest_framework.response import Response

from brouwers.general.constants import CountryChoices

from ..constants import CART_SESSION_KEY
from ..models import Cart, ShippingCost
from ..payments.sisow.service import get_ideal_banks
from .serializers import CartSerializer, iDealBankSerializer


class IdealBanksView(views.APIView):
    def get(self, request):
        serializer = iDealBankSerializer(
            instance=get_ideal_banks(),
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class CartView(views.APIView):
    def get(self, request):
        cart = Cart.objects.open().for_request(request).last()

        if cart is None:
            if request.user.is_authenticated:
                cart = Cart.objects.create(user=request.user)
            else:
                cart = Cart.objects.create()
            request.session[CART_SESSION_KEY] = cart.id

        serializer = CartSerializer(instance=cart)
        return Response(serializer.data)


class GetShippingCostsView(views.APIView):
    def get(self, request: Request):
        cart_id: str | None = request.GET.get("cart_id")
        match cart_id:
            case None:
                raise serializers.ValidationError(
                    {"cart_id": "cart_id query param is required."}, code="required"
                )
            case str() if cart_id.isdigit():
                cart = (
                    Cart.objects.open().for_request(request).filter(pk=cart_id).first()
                )
            case _:
                raise serializers.ValidationError({"cart_id": "Invalid cart ID."})
        if cart is None:
            raise serializers.ValidationError({"cart_id": "Invalid cart ID."})
        assert isinstance(cart, Cart)

        try:
            country = CountryChoices(request.GET.get("country"))
        except ValueError:
            raise serializers.ValidationError({"country": "Invalid country."})

        # now the cart and country have been validated, calculate the price
        total_weight_in_grams = cart.weight

        # TODO
        price = ShippingCost.objects.get_price(
            country=country, weight=total_weight_in_grams
        )
        assert price is not None

        if total_weight_in_grams < 1000:
            number = number_format(total_weight_in_grams)
            formatted_weight = f"{number} g"
        else:
            number = number_format(total_weight_in_grams / 1000)
            formatted_weight = f"{number} kg"

        return Response(
            {
                "weight": formatted_weight,
                "price": str(price),
            }
        )
