import uuid

from ...models import Payment
from .client import Client


def attempt_capture(payment: Payment) -> bool:
    """
    Capture the payment if the buyer approved the order in Paypal.
    """
    order_id = payment.data["paypal_order"]["id"]
    # check if we need to generate a capture request ID
    if not (request_id := payment.data.get("paypal_capture_request_id")):
        request_id = str(uuid.uuid4())
        payment.data["paypal_capture_request_id"] = request_id
        payment.save(update_fields=["data"])

    # check the order state
    captured = False
    with Client() as client:
        paypal_order = client.get_order(order_id)
        if paypal_order.status == "APPROVED":
            client.capture(paypal_order, request_id)
            captured = True

        # TODO: check the amounts again to prevent partial payments? is that
        # even possible?
        payment.data["paypal_order"]["status"] = paypal_order.status
        payment.mark_paid()
    return captured
