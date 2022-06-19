from decimal import Decimal

from django.db import models
from django.templatetags.l10n import localize
from django.utils.translation import ugettext_lazy as _

from ..payments.constants import PaymentMethods
from .utils import get_max_order, get_payment_reference

__all__ = ["PaymentMethod", "Payment"]


class PaymentMethod(models.Model):
    name = models.CharField(_("name"), max_length=50)
    method = models.CharField(
        _("method"), max_length=50, choices=PaymentMethods.choices, unique=True
    )
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

    This tracks all information needed to debug payment issues.
    """

    reference = models.CharField(
        _("reference"),
        max_length=16,
        unique=True,
        default=get_payment_reference,
        help_text=_("A unique payment reference"),
    )
    payment_method = models.ForeignKey(
        "PaymentMethod", verbose_name=_("Payment method used"), on_delete=models.PROTECT
    )
    amount = models.IntegerField(
        _("amount"), help_text=_("Amount to be paid, in eurocents.")
    )
    cart = models.ForeignKey(
        "Cart",
        verbose_name=_("shopping cart"),
        help_text=_("The shopping cart that generated this payment."),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    data = models.JSONField(
        _("payment data"),
        default=dict,
        blank=True,
        help_text=_("The exact payment data is provider-specific"),
    )

    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return self.reference

    def format_amount(self) -> str:
        amount_in_euro = Decimal(self.amount) / 100
        return "€ {amount}".format(amount=localize(amount_in_euro))
