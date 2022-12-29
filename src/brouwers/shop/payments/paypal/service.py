import uuid
from decimal import Decimal
from typing import Optional

from django.http import HttpRequest
from django.urls import reverse
from django.utils import translation

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from ...models import Payment, ShopConfiguration

BASE_URLS = {
    "live": "https://api-m.paypal.com",
    "sandbox": "https://api-m.sandbox.paypal.com",
}


def start_payment(
    payment: Payment, request: Optional[HttpRequest] = None, next_page=""
) -> str:
    assert request
    config = ShopConfiguration.get_solo()
    base_url = BASE_URLS["live" if not config.paypal_sandbox else "sandbox"]

    # get token
    client = BackendApplicationClient(client_id=config.paypal_client_id)
    session = OAuth2Session(client=client)
    session.fetch_token(
        token_url=f"{base_url}/v1/oauth2/token",
        client_id=config.paypal_client_id,
        client_secret=config.paypal_secret,
    )

    # TODO: rename or use pp specific URL
    payment_callback = reverse("shop:sisow-payment-callback", kwargs={"pk": payment.pk})
    payment_cancel = f"/winkel/payment/{payment.pk}/cancelled"

    response = session.post(
        f"{base_url}/v2/checkout/orders",
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "reference_id": payment.reference,
                    "amount": {
                        "currency_code": "EUR",
                        "value": str(
                            payment.amount * Decimal("0.01")
                        ),  # quantize to two decimal places
                    },
                    # "invoice_id": "",
                }
            ],
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                        "payment_method_selected": "PAYPAL",
                        "brand_name": "Modelbrouwers.nl",  # TODO -> configure
                        "locale": translation.get_language(),
                        "shipping_preference": "SET_PROVIDED_ADDRESS",
                        "user_action": "PAY_NOW",
                        "return_url": request.build_absolute_uri(payment_callback),
                        "cancel_url": request.build_absolute_uri(payment_cancel),
                    }
                }
            },
        },
        headers={
            "PayPal-Request-Id": str(uuid.uuid4()),  # TODO -> store this
        },
    )
    response.raise_for_status()
    links = response.json()["links"]

    redirect_url = next(link["href"] for link in links if link["rel"] == "payer-action")
    return redirect_url
