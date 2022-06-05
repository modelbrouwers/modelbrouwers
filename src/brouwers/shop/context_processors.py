from typing import Dict, Optional, TypedDict

from django.http import HttpRequest
from django.urls import reverse

from .models import Cart


class CartContext(TypedDict):
    cart: Optional[Cart]
    cart_url: str


def cart(request: HttpRequest) -> CartContext:
    cart = Cart.objects.open().for_request(request).last()
    return {
        "cart": cart,
        "cart_url": reverse("shop:cart-detail", kwargs={"pk": cart.pk}) if cart else "",
    }
