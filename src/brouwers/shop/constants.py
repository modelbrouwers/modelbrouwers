from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices

TWO_DIGITS = Decimal("0.01")

CART_SESSION_KEY = "cart_id"
ORDERS_SESSION_KEY = "order_ids"


class WeightUnits(DjangoChoices):
    gram = ChoiceItem("g", _("Gram"))
    kilogram = ChoiceItem("kg", _("Kilogram"))


class LengthUnits(DjangoChoices):
    mm = ChoiceItem("mm", _("Milimetre"))
    cm = ChoiceItem("cm", _("Centimetre"))
    m = ChoiceItem("m", _("Metre"))


class CartStatuses(DjangoChoices):
    open = ChoiceItem("open", _("Open"))
    processing = ChoiceItem("processing", _("Processing"))
    closed = ChoiceItem("closed", _("Closed"))


class OrderStatuses(DjangoChoices):
    received = ChoiceItem("received", _("Received"))
    processing = ChoiceItem("processing", _("Processing"))
    shipped = ChoiceItem("shipped", _("Shipped"))
    cancelled = ChoiceItem("cancelled", _("Cancelled"))


class PaymentStatuses(DjangoChoices):
    pending = ChoiceItem("pending", _("Pending"))
    completed = ChoiceItem("completed", _("Completed"))
    cancelled = ChoiceItem("cancelled", _("Cancelled"))
