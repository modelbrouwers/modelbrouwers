from django.core.cache import caches

from ...models import Order, Payment, ShopConfiguration


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.cache = caches["default"]

    def session(self):
        pass
