from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = "brouwers.shop"

    def ready(self):
        # register the payment options
        from .payments import payment_options  # noqa
