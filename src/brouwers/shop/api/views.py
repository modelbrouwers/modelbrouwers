from rest_framework import views
from rest_framework.response import Response

from ..constants import CART_SESSION_KEY
from ..models import Cart
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
