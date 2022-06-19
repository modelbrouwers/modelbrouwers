from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext, gettext_lazy as _

from brouwers.general.fields import CountryField

from ..constants import OrderStatuses


class Address(models.Model):
    street = models.CharField(_("street name"), max_length=255)
    number = models.CharField(_("house number"), max_length=30, blank=True)
    postal_code = models.CharField(_("postal code"), max_length=50)
    city = models.CharField(_("city"), max_length=255)
    country = CountryField()

    # company details
    company = models.CharField(_("company"), max_length=255, blank=True)
    chamber_of_commerce = models.CharField(
        _("chamber of commerce number"), max_length=50, blank=True
    )

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")

    def __str__(self):
        bits = [
            f"{self.street} {self.number}".strip(),
            self.postal_code,
            self.city,
            self.country,
        ]
        return ", ".join(bits)


class Order(models.Model):
    cart = models.ForeignKey(
        "Cart", on_delete=models.PROTECT, verbose_name=_("shopping cart")
    )
    payment = models.ForeignKey(
        "Payment", on_delete=models.PROTECT, verbose_name=_("payment instance")
    )
    status = models.CharField(_("status"), max_length=50, choices=OrderStatuses)
    # TODO: add django-privates and field for invoices

    # personal details
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(_("email"))
    phone = models.CharField(_("phone number"), max_length=100, blank=True)

    # addresses
    delivery_address = models.OneToOneField(
        "Address",
        on_delete=models.PROTECT,
        related_name="delivery_order",
        help_text=_("Address for delivery"),
    )
    invoice_address = models.OneToOneField(
        "Address",
        on_delete=models.SET_NULL,
        related_name="invoice_order",
        blank=True,
        null=True,
    )

    # metadata
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return _("Order {pk}").format(pk=self.pk)

    def clean(self):
        if self.payment.cart and self.payment.cart != self.cart:
            raise ValidationError(_("Order and payment cart must be identical."))

    @property
    def reference(self) -> str:
        if not self.payment:
            return gettext("(no reference yet)")
        return self.payment.reference
