import logging
import uuid

from django.db import transaction
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from ...models import Payment
from ..utils import get_next_page
from .client import Client

logger = logging.getLogger(__name__)


class ReturnView(View):
    def get(self, request: HttpRequest, pk: int):
        with transaction.atomic():
            locking_qs = Payment.objects.select_for_update()
            payment = get_object_or_404(locking_qs, pk=pk)

            if payment.payment_method.method != "paypal_standard":
                raise Http404("Invalid payment reference")

            order_id = request.GET.get("token", "")
            try:
                paypal_order_id = payment.data["paypal_order"]["id"]
                if paypal_order_id != order_id:
                    logger.warning(
                        "Token ID from URL and order do not match, payment %d",
                        payment.pk,
                    )
                    raise ValueError("Order ID mismatch")
            except (KeyError, ValueError) as exc:
                raise Http404("Invalid payment reference") from exc

            # check if we need to generate a capture request ID
            if not (request_id := payment.data.get("paypal_capture_request_id")):
                request_id = str(uuid.uuid4())
                payment.data["paypal_capture_request_id"] = request_id
                payment.save(update_fields=["data"])

        # check the order state
        with Client() as client:
            paypal_order = client.get_order(order_id)
            if paypal_order.status != "COMPLETED":
                client.capture(paypal_order, request_id)
            # TODO: mark order as paid if full sum is received

        next_page = get_next_page(self.request) or reverse("shop:index")
        return redirect(next_page)


class CancelView(View):
    def get(self, request: HttpRequest, pk: int):
        import bpdb

        bpdb.set_trace()
