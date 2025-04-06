from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from furl import furl

from brouwers.general.fields import CountryField

from ..constants import DeliveryMethods, OrderStatuses
from .utils import get_random_reference

if TYPE_CHECKING:
    from .payments import Payment


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


def get_order_reference():
    """
    Generate a random but unique reference.
    """
    MAX_ATTEMPTS = 100  # ensure we have finite loops (while is evil)
    iterations = 0

    for _ in range(MAX_ATTEMPTS):  # noqa: F402
        iterations += 1
        reference = get_random_reference()
        exists = Order.objects.only("pk").filter(reference=reference).exists()
        if exists is False:
            return reference

    # loop ran all the way to the end without finding unused reference
    # (otherwise it would have returned)
    raise RuntimeError(
        f"Could not get a unused reference after {iterations} attempts!"
    )  # pragma: no cover


class Order(models.Model):
    cart = models.OneToOneField(
        "Cart", on_delete=models.PROTECT, verbose_name=_("shopping cart")
    )
    status = models.CharField(_("status"), max_length=50, choices=OrderStatuses.choices)
    reference = models.CharField(
        _("reference"),
        max_length=16,
        unique=True,
        default=get_order_reference,
        help_text=_("A unique order reference"),
    )
    # TODO: add django-privates and field for invoices

    # personal details
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(_("email"))
    phone = models.CharField(_("phone number"), max_length=100, blank=True)

    # addresses
    delivery_method = models.CharField(
        _("delivery method"),
        max_length=20,
        choices=DeliveryMethods.choices,
    )
    delivery_address = models.OneToOneField(
        "Address",
        on_delete=models.PROTECT,
        related_name="delivery_order",
        help_text=_("Address for delivery"),
        blank=True,
        null=True,
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
    language = models.CharField(
        _("language"), max_length=10, default="nl", choices=settings.LANGUAGES
    )

    shipping_costs = models.DecimalField(
        _("shipping costs"),
        decimal_places=2,
        max_digits=6,
        blank=True,
        null=True,
    )

    payment: "Payment"

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        constraints = [
            models.CheckConstraint(
                name="delivery_address_when_shipping",
                check=(
                    Q(
                        delivery_method=DeliveryMethods.mail,
                        delivery_address__isnull=False,
                    )
                    | ~Q(delivery_method=DeliveryMethods.mail)
                ),
                violation_error_message=_(
                    "A delivery address must be specified when deliverying via mail."
                ),
            )
        ]

    def __str__(self):
        return _("Order {pk}").format(pk=self.pk)

    def get_full_name(self) -> str:
        bits = [self.first_name, self.last_name]
        return " ".join(bits).strip()

    def get_confirmation_link(self) -> str:
        path = reverse("shop:checkout", kwargs={"path": "confirmation"})
        return furl(path).set({"orderId": self.pk}).url
