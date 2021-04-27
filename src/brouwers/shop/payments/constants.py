from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices

from .sisow.constants import Payments as SisowPayments


class PaymentProviders(DjangoChoices):
    paypal = ChoiceItem("paypal", _("Paypal"))
    bank_transfer = ChoiceItem("bank_transfer", _("Bank transfer"))


class PaymentMethods(SisowPayments, PaymentProviders):
    pass
