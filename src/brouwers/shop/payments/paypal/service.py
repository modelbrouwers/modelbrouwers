from django.http import HttpRequest
from django.urls import reverse
from django.utils import translation

from furl import furl

from ...models import Payment
from .client import Client


def _build_callback_url(
    name: str, kwargs: dict, request: HttpRequest, next_page: str
) -> str:
    path = reverse(name, kwargs=kwargs)
    url = request.build_absolute_uri(path)
    if next_page:
        url = furl(url).set({"next": next_page}).url
    return url


def start_payment(
    payment: Payment,
    request: HttpRequest,
    next_page="",
) -> str:

    payment_return = _build_callback_url(
        "shop:paypal-return",
        {"pk": payment.pk},
        request,
        next_page=next_page,
    )
    payment_cancel = _build_callback_url(
        "shop:paypal-cancel",
        {"pk": payment.pk},
        request,
        next_page=next_page,
    )

    with Client() as client:
        paypal_order = client.create_order(
            reference=payment.reference,
            amount=payment.amount,
            locale=translation.get_language(),
            return_url=payment_return,
            cancel_url=payment_cancel,
            request_id=payment.data["paypal_request_id"],
        )

    payment.data["paypal_order"] = {"id": paypal_order.id}
    payment.save(update_fields=["data"])
    return paypal_order.get_redirect_url()
