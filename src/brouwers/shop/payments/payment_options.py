import logging

from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from ..models import Payment
from .registry import Plugin, register

logger = logging.getLogger(__name__)


@register("bank_transfer")
class BankTransfer(Plugin):
    verbose_name = _("Bank transfer")

    def start_payment(self, payment: Payment) -> None:
        logger.info(
            "Initiating payment flow for payment %d, using plugin %s",
            payment.id,
            self.identifier,
        )
        return None


@register("paypal_standard")
class PayPalStandard(Plugin):
    verbose_name = _("PayPal standard")

    def start_payment(self, payment: Payment) -> HttpResponseRedirect:
        logger.info(
            "Initiating payment flow for payment %d, using plugin %s",
            payment.id,
            self.identifier,
        )
        raise NotImplementedError("TODO")
