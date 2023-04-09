import logging
import uuid
from typing import cast

from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..models import Order, Payment, ShopConfiguration
from .paypal.service import start_payment as start_paypal_payment
from .registry import PaymentContext, Plugin, register
from .sisow.constants import SisowMethods
from .sisow.service import start_payment as start_sisow_payment

logger = logging.getLogger(__name__)


@register("bank_transfer")
class BankTransfer(Plugin):
    verbose_name = _("Bank transfer")

    def start_payment(self, payment: Payment, context: PaymentContext) -> None:
        return None

    def get_confirmation_message(self, order: Order) -> str:
        config = cast(ShopConfiguration, ShopConfiguration.get_solo())
        return config.bank_transfer_instructions


@register("paypal_standard")
class PayPalStandard(Plugin):
    verbose_name = _("PayPal standard")

    @transaction.atomic
    def start_payment(
        self, payment: Payment, context: PaymentContext
    ) -> HttpResponseRedirect:
        # track some metadata that is paypal specific
        locking_qs = Payment.objects.select_for_update().filter(pk=payment.pk)
        payment = locking_qs.get()

        order = context.get("order")
        if order is not None:
            payment.data["order"] = {"id": order.pk}
        payment.data["paypal_request_id"] = str(uuid.uuid4())
        payment.save(update_fields=["data"])

        checkout_url = reverse("shop:checkout", kwargs={"path": "payment"})
        redirect_url = start_paypal_payment(
            payment=payment,
            request=context["request"],
            success_page=context.get("next_page", ""),
            cancel_page=checkout_url,
        )
        return HttpResponseRedirect(redirect_url)


class SisowPlugin(Plugin):
    sisow_method: str

    def start_payment(
        self, payment: Payment, context: PaymentContext
    ) -> HttpResponseRedirect:
        payment.data["sisow_method"] = self.sisow_method
        payment.save(update_fields=["data"])
        redirect_url = start_sisow_payment(
            payment=payment,
            request=context["request"],
            next_page=context.get("next_page", ""),
        )
        return HttpResponseRedirect(redirect_url)


@register("sisow_ideal")
class SisowIDeal(SisowPlugin):
    verbose_name = _("iDeal")
    sisow_method = cast(str, SisowMethods.ideal)


@register("sisow_sofort")
class SisowSofort(SisowPlugin):
    verbose_name = _("Sofort")
    sisow_method = cast(str, SisowMethods.sofort)


@register("sisow_mistercash")
class SisowMrCash(SisowPlugin):
    verbose_name = _("Mister Cash")
    sisow_method = cast(str, SisowMethods.mistercash)
