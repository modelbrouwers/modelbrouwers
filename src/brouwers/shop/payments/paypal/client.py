from decimal import Decimal
from typing import cast

from django.conf import settings
from django.core.cache import caches
from django.utils.functional import cached_property

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from ...models import ShopConfiguration
from .api_models import PaypalOrder

BASE_URLS = {
    "live": "https://api-m.paypal.com",
    "sandbox": "https://api-m.sandbox.paypal.com",
}

TOKEN_CACHE_KEY = "paypal:access-token"


class Client:
    _session: OAuth2Session | None = None

    def __init__(self):
        self.cache = caches["default"]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._session is None:
            return
        self.session.close()

    @cached_property
    def config(self):
        return cast(ShopConfiguration, ShopConfiguration.get_solo())

    @cached_property
    def base_url(self) -> str:
        alias = "live" if not self.config.paypal_sandbox else "sandbox"
        return BASE_URLS[alias]

    @property
    def session(self) -> OAuth2Session:
        if self._session is None:
            client = BackendApplicationClient(client_id=self.config.paypal_client_id)
            # check if we still have a token
            token = self.cache.get(TOKEN_CACHE_KEY) or None
            session = OAuth2Session(client=client, token=token)
            if token is None:
                token = session.fetch_token(
                    token_url=f"{self.base_url}/v1/oauth2/token",
                    client_id=self.config.paypal_client_id,
                    client_secret=self.config.paypal_secret,
                )
                # cache invalidate 10 seconds before expiry to account for possible clock drift
                ttl = token["expires_in"] - 10
                self.cache.set(TOKEN_CACHE_KEY, token, timeout=ttl)
            self._session = session
        return self._session

    def create_order(
        self,
        reference: str,
        amount: int,
        locale: str,
        return_url: str,
        cancel_url: str,
        request_id: str,
    ) -> PaypalOrder:
        # quantize the amount in cents to two decimal places
        _amount = str(amount * Decimal("0.01"))

        response = self.session.post(
            f"{self.base_url}/v2/checkout/orders",
            json={
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "invoice_id": reference,
                        "amount": {
                            "currency_code": "EUR",
                            "value": _amount,
                        },
                    }
                ],
                "payment_source": {
                    "paypal": {
                        "experience_context": {
                            "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                            "payment_method_selected": "PAYPAL",
                            "brand_name": settings.SHOP_BRAND_NAME,
                            "locale": locale,
                            "shipping_preference": "NO_SHIPPING",
                            "user_action": "PAY_NOW",
                            "return_url": return_url,
                            "cancel_url": cancel_url,
                        }
                    }
                },
            },
            headers={"PayPal-Request-Id": request_id},
        )
        response.raise_for_status()
        order = PaypalOrder(**response.json())
        return order

    def get_order(self, order_id: str) -> PaypalOrder:
        response = self.session.get(f"{self.base_url}/v2/checkout/orders/{order_id}")
        response.raise_for_status()
        return PaypalOrder(**response.json())

    def capture(self, order: PaypalOrder, request_id: str) -> PaypalOrder:
        url = order.get_capture_url()
        response = self.session.post(
            url,
            headers={
                "Content-Type": "application/json",
                "PayPal-Request-Id": request_id,
            },
        )
        response.raise_for_status()
        return PaypalOrder(**response.json())
