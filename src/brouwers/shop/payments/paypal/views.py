import logging
import uuid

from django.db import transaction
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from ...constants import CART_SESSION_KEY, CartStatuses
from ...models import Payment
from ..utils import get_next_page
from .client import Client
from .utils import attempt_capture

logger = logging.getLogger(__name__)


class ValidatePaymentMixin:
    request: HttpRequest

    def validate_payment(self, payment: Payment) -> str:
        """
        Raise an exception if no valid token could be correlated with the payment.
        """
        if payment.payment_method.method != "paypal_standard":
            raise Http404("Invalid payment reference")

        order_id = self.request.GET.get("token", "")
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

        return order_id


class ReturnView(ValidatePaymentMixin, View):
    def get(self, request: HttpRequest, pk: int):
        with transaction.atomic():
            locking_qs = Payment.objects.select_for_update()
            payment = get_object_or_404(locking_qs, pk=pk)
            self.validate_payment(payment)

            captured = attempt_capture(payment)
            logger.info(
                "Payment %d capture succeeded: %r",
                payment.pk,
                captured,
                extra={
                    "id": payment.pk,
                    "captured": captured,
                },
            )

        next_page = get_next_page(request) or reverse("shop:index")
        return redirect(next_page)


class CancelView(ValidatePaymentMixin, View):
    def get(self, request: HttpRequest, pk: int):
        payment = get_object_or_404(
            Payment.objects.select_related("order", "order__cart"),
            pk=pk,
        )
        order_id = self.validate_payment(payment)
        # check the order state
        with Client() as client:
            paypal_order = client.get_order(order_id)
            logger.info(
                "Cancelled payment %d has status %s.",
                payment.pk,
                paypal_order.status,
            )
            # by default, we have 3 hours to redirect the payer to the approval, and there's
            # no explicit cancel operation for orders, so we can just let it time out?

        payment.cancel()

        # re-add the cart to the session
        assert (
            payment.historical_order is not None
        ), "Cancelling a payment must set the historical order"
        cart = payment.historical_order.cart
        cart.status = CartStatuses.open
        cart.save(update_fields=["status"])
        request.session[CART_SESSION_KEY] = cart.id

        next_page = get_next_page(request) or reverse("shop:index")
        return redirect(next_page)
