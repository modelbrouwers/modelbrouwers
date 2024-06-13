from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

TWO_DIGITS = Decimal("0.01")

CART_SESSION_KEY = "cart_id"
ORDERS_SESSION_KEY = "order_ids"


class WeightUnits(models.TextChoices):
    gram = "g", _("Gram")
    kilogram = "kg", _("Kilogram")


class LengthUnits(models.TextChoices):
    mm = "mm", _("Milimetre")
    cm = "cm", _("Centimetre")
    m = "m", _("Metre")


class CartStatuses(models.TextChoices):
    open = "open", _("Open")
    processing = "processing", _("Processing")
    closed = "closed", _("Closed")


class OrderStatuses(models.TextChoices):
    received = "received", _("Received")
    processing = "processing", _("Processing")
    shipped = "shipped", _("Shipped")
    cancelled = "cancelled", _("Cancelled")


class PaymentStatuses(models.TextChoices):
    pending = "pending", _("Pending")
    completed = "completed", _("Completed")
    cancelled = "cancelled", _("Cancelled")


class ShippingMethods(models.TextChoices):
    pickup = "pickup", _("Pick up")
    mail = "mail", _("By mail")
