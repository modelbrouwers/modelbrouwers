from typing import Optional

from django.contrib import messages
from django.http import HttpRequest
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _

from ..constants import CART_SESSION_KEY, CartStatuses
from ..models import Payment


def get_next_page(request: HttpRequest, next_param="next") -> Optional[str]:
    if not (next_page := request.GET.get(next_param)):
        return None

    url_is_safe = url_has_allowed_host_and_scheme(
        url=next_page,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )
    if not url_is_safe:
        return None

    return next_page


def on_payment_failure(payment: Payment, request: HttpRequest) -> None:
    """
    Hook executed when a payment was not deemed succesful.

    1. Cancel the payment for our internal bookkeeping
    2. Ensure that the shopping cart is reinstated so that a new payment attempt can be
       made
    """
    payment.cancel()

    # re-add the cart to the session
    assert (
        payment.historical_order is not None
    ), "Cancelling a payment must set the historical order"
    cart = payment.historical_order.cart
    cart.status = CartStatuses.open
    cart.save(update_fields=["status"])
    request.session[CART_SESSION_KEY] = cart.id

    messages.error(request, _("Your payment was not received (yet) - please retry."))
