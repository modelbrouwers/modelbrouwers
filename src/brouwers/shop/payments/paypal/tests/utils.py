from copy import deepcopy
from unittest.mock import patch

from django.conf import settings
from django.core.cache.backends.dummy import DummyCache
from django.test import override_settings

from ....models import ShopConfiguration


def patch_config(**overrides):
    fields = {
        "paypal_sandbox": False,
        "paypal_client_id": "dummy-client-id",
        "paypal_secret": "dummy-client-secret",
        **overrides,
    }
    patcher = patch(
        "brouwers.shop.payments.paypal.client.ShopConfiguration.get_solo",
        return_value=ShopConfiguration(**fields),
    )
    return patcher


class PaypalClientCache(DummyCache):
    def __init__(self, host, params, *args, **kwargs):
        super().__init__(host, params, *args, **kwargs)
        self.options = params["OPTIONS"]

    def get(self, key, *args, **kwargs):
        if key == "paypal:access-token" and (token := self.options.get("token")):
            return token
        return super().get(key, *args, **kwargs)


def patch_cache(options=None, backend=None):
    mock_backend = f"{PaypalClientCache.__module__}.{PaypalClientCache.__qualname__}"
    backend = backend or mock_backend
    new_setting = {
        **deepcopy(settings.CACHES),
        "default": {
            "BACKEND": backend,
            "OPTIONS": options or {},
        },
    }
    return override_settings(CACHES=new_setting)
