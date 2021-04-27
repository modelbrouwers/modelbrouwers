from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices

TWO_DIGITS = Decimal("0.01")


class WeightUnits(DjangoChoices):
    gram = ChoiceItem("g", _("Gram"))
    kilogram = ChoiceItem("kg", _("Kilogram"))


class CartStatuses(DjangoChoices):
    open = ChoiceItem("open", _("Open"))
    paid = ChoiceItem("paid", _("Paid"))
