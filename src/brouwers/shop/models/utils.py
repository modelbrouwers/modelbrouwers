from django.db import models
from django.utils.crypto import get_random_string


def get_max_order() -> int:
    from .payments import PaymentMethod

    max_order = PaymentMethod.objects.aggregate(max=models.Max("order"))["max"] or 0
    return max_order + 1


def get_payment_reference() -> str:
    """
    Generate a payment reference.

    TODO: can be made pluggable, if needed.
    """
    from .payments import Payment

    START = "30000"
    max_reference = (
        Payment.objects.aggregate(max=models.Max("reference"))["max"] or START
    )
    new_reference = str(int(max_reference) + 1)
    return new_reference


def get_random_reference():
    # 32 characters with length 6 -> 32^6 possible combinations.
    # that's roughly one billion combinations before we run out of options.
    random_string = get_random_string(
        length=6, allowed_chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    )
    return f"MB-{random_string}"
