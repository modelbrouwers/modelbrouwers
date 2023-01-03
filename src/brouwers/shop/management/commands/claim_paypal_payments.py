from django.core.management import BaseCommand
from django.db import transaction

from ...models import Payment
from ...payments.paypal.utils import attempt_capture

PAYPAL_METHOD = "paypal_standard"


NON_CAPTURABLE_STATUSES = [
    "CREATED",
    "SAVED",
    "VOIDED",
    "COMPLETED",
    "PAYER_ACTION_REQUIRED",
]


class Command(BaseCommand):
    help = "Shop payments - check pending Paypal payments"

    @transaction.atomic()
    def handle(self, **options):
        payments = Payment.objects.filter(payment_method__method=PAYPAL_METHOD).exclude(
            data__paypal_order__has_key="status",
            data__paypal_order__status__in=NON_CAPTURABLE_STATUSES,
        )
        succeeded = []
        for payment in payments.select_for_update():
            captured = attempt_capture(payment)
            if captured:
                succeeded.append(payment)

        ids = ", ".join([str(payment.pk) for payment in succeeded]) or "-"
        self.stdout.write(f"Captured payments: {ids}.")
