from decimal import Decimal

from django.db import models, transaction
from django.templatetags.l10n import localize
from django.utils.translation import ugettext_lazy as _

from ..constants import PaymentStatuses
from .utils import get_max_order, get_payment_reference

__all__ = ["PaymentMethod", "Payment"]


class PaymentMethod(models.Model):
    name = models.CharField(_("name"), max_length=50)
    method = models.CharField(_("method"), max_length=50, unique=True)
    logo = models.ImageField(_("logo"), upload_to="shop/payment_methods/", blank=True)
    enabled = models.BooleanField(
        _("enabled"),
        default=False,
        help_text=_("Whether the payment method can be used at checkout or not."),
    )
    order = models.PositiveSmallIntegerField(_("ordering"), default=get_max_order)

    class Meta:
        verbose_name = _("payment method")
        verbose_name_plural = _("payment methods")

    def __str__(self):
        return self.name


class Payment(models.Model):
    """
    Represent payment for an order.

    An order is paid by a single payment, tracked via the ``order`` o2o-field. It's
    possible payments are cancelled, in which case the return/cancel flow will related
    them accordingly.

    This tracks all information needed to debug payment issues.
    """

    order = models.OneToOneField(
        "Order",
        on_delete=models.CASCADE,  # deleting the order deletes the payment with it
        null=True,
        blank=True,
        verbose_name=_("order"),
        help_text=_("The order being paid by this payment."),
    )
    payment_method = models.ForeignKey(
        "PaymentMethod", verbose_name=_("Payment method used"), on_delete=models.PROTECT
    )
    amount = models.IntegerField(
        _("amount"), help_text=_("Amount to be paid, in eurocents.")
    )
    status = models.CharField(
        _("status"),
        max_length=50,
        choices=PaymentStatuses.choices,
        default=PaymentStatuses.pending,
    )
    reference = models.CharField(
        _("reference"),
        max_length=16,
        unique=True,
        default=get_payment_reference,
        help_text=_("A unique payment reference"),
    )
    data = models.JSONField(
        _("payment data"),
        default=dict,
        blank=True,
        help_text=_("The exact payment data is provider-specific"),
    )
    historical_order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="historical_payments",
        verbose_name=_("historical order"),
        help_text=_(
            "Order this payment was for, in case it was cancelled/aborted. You cannot "
            "set order and historical order at the same time.",
        ),
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(order__isnull=False, historical_order__isnull=True)
                    | models.Q(order__isnull=True, historical_order__isnull=False)
                ),
                name="order_or_historical_order",
            ),
        ]

    def __str__(self):
        return self.reference

    def format_amount(self) -> str:
        amount_in_euro = Decimal(self.amount) / 100
        return "€ {amount}".format(amount=localize(amount_in_euro))

    def mark_paid(self) -> None:
        if self.status == PaymentStatuses.completed:
            return

        assert (
            self.status != PaymentStatuses.cancelled
        ), "Cannot mark cancelled payment as completed"
        assert self.order_id is not None, "Cannot complete historical payments"

        self.status = PaymentStatuses.completed
        self.save(update_fields=["status"])

    @transaction.atomic()
    def cancel(self) -> None:
        if self.status == PaymentStatuses.cancelled:
            return

        self.historical_order = self.order
        self.order = None
        self.status = PaymentStatuses.cancelled
        self.save()
