from typing import Optional

from django.http import HttpRequest
from django.http.response import HttpResponseBase

from ..models import Payment
from .registry import register

__all__ = ["start_payment", "register"]


def start_payment(
    payment: "Payment", request: HttpRequest, **context
) -> Optional[HttpResponseBase]:
    context["request"] = request
    plugin_id = payment.payment_method.method
    plugin = register[plugin_id]
    return plugin.start_payment(payment, context)
