import logging

from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from ..models import Order, Payment, ShopConfiguration
from .paypal.service import start_payment as start_paypal_payment
from .registry import Plugin, register
from .sisow.service import start_payment as start_sisow_payment

logger = logging.getLogger(__name__)


@register("bank_transfer")
class BankTransfer(Plugin):
    verbose_name = _("Bank transfer")

    def start_payment(self, payment: Payment, context: dict) -> None:
        logger.info(
            "Initiating payment flow for payment %d, using plugin %s",
            payment.id,
            self.identifier,
        )
        return None

    def get_confirmation_message(self, order: Order) -> str:
        config = ShopConfiguration.get_solo()
        return config.bank_transfer_instructions


@register("paypal_standard")
class PayPalStandard(Plugin):
    verbose_name = _("PayPal standard")

    def start_payment(self, payment: Payment, context: dict) -> HttpResponseRedirect:
        logger.info(
            "Initiating payment flow for payment %d, using plugin %s",
            payment.id,
            self.identifier,
        )
        redirect_url = start_paypal_payment(
            payment=payment,
            request=context.get("request"),
            next_page=context.get("next_page", ""),
        )
        return HttpResponseRedirect(redirect_url)


class SisowPlugin(Plugin):
    sisow_method: str

    def start_payment(self, payment: Payment, context: dict) -> HttpResponseRedirect:
        logger.info(
            "Initiating payment flow for payment %d, using plugin %s",
            payment.id,
            self.identifier,
        )
        payment.data["sisow_method"] = self.sisow_method
        payment.save(update_fields=["data"])
        redirect_url = start_sisow_payment(
            payment=payment,
            request=context.get("request"),
            next_page=context.get("next_page", ""),
        )
        return HttpResponseRedirect(redirect_url)


@register("sisow_ideal")
class SisowIDeal(SisowPlugin):
    verbose_name = _("iDeal")
    sisow_method = "ideal"


@register("sisow_sofort")
class SisowSofort(SisowPlugin):
    verbose_name = _("Sofort")
    sisow_method = "sofort"


@register("sisow_mistercash")
class SisowMrCash(SisowPlugin):
    verbose_name = _("Mister Cash")
    sisow_method = "mistercash"
