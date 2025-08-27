import logging

from django.http import HttpRequest
from django.http.response import HttpResponseBase

from ..models import Payment
from .registry import register

logger = logging.getLogger(__name__)

__all__ = ["start_payment", "register"]


def start_payment(
    payment: Payment, request: HttpRequest, **context
) -> HttpResponseBase | None:
    context["request"] = request
    plugin_id = payment.payment_method.method
    plugin = register[plugin_id]
    logger.info(
        "Initiating payment flow for payment %d, using plugin %s",
        payment.pk,
        plugin.identifier,
    )
    return plugin.start_payment(payment, context)
