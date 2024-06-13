from decimal import Decimal
from typing import Callable

from django.db import models
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from brouwers.general.constants import CountryChoices
from brouwers.general.fields import CountryField


class ShippingCostManager(models.Manager):

    def get_price(self, country: CountryChoices | str, weight: int) -> None | Decimal:
        qs = (
            self.filter(country=country)
            .exclude(max_weight__lt=weight)
            .order_by("max_weight")
            .values_list("price", flat=True)
        )
        return qs.first()


class ShippingCost(models.Model):
    """
    Models the price of shipping up to a given weight, for a given country.

    XXX: how to handle orders to a country without costs configured?
    XXX: how to handle orders that fall outside of the weight range?
    """

    label = models.CharField(
        _("label"),
        max_length=100,
        help_text=_("Descriptive label, e.g. 'enveloppe' or 'small package'."),
    )
    country = CountryField(
        verbose_name=_("country"),
        help_text=_("Country to ship the order to."),
    )
    max_weight = models.PositiveSmallIntegerField(
        _("maximum weight"),
        help_text=_(
            "Maximum weight (in grams) for orders to match this shipping cost."
        ),
    )
    price = models.DecimalField(
        _("price"),
        max_digits=5,
        decimal_places=2,
        help_text=_("Shipping cost for this weight limit, including VAT."),
    )

    objects = ShippingCostManager()

    get_country_display: Callable[[], str]

    class Meta:
        verbose_name = _("shipping cost")
        verbose_name_plural = _("shipping costs")
        constraints = [
            models.UniqueConstraint(
                fields=("country", "max_weight"),
                name="unique_ranges",
            ),
        ]

    def __str__(self) -> str:
        return _("{country} - {label}, ≤ {weight}: € {price}").format(
            label=self.label,
            country=self.get_country_display(),
            weight=self.format_weight(),
            price=formats.number_format(self.price, decimal_pos=2),
        )

    def format_weight(self) -> str:
        if self.max_weight >= 1000:
            value = round(self.max_weight / 1000, 2)
            return _("{} kg").format(formats.number_format(value, decimal_pos=2))
        return _("{} g").format(self.max_weight)
