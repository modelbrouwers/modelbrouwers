from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel

from ..payments.constants import PaymentMethods


@python_2_unicode_compatible
class ShopConfiguration(SingletonModel):
    sisow_test_mode = models.BooleanField(_("sisow test mode"), default=False)
    sisow_merchant_id = models.CharField(_("sisow merchant ID"), max_length=100, blank=True)
    sisow_merchant_key = models.CharField(_("sisow merchant key"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Shop configuration")

    def __str__(self):
        return "Shop configuration"


def get_max_order() -> int:
    max_order = PaymentMethod.objects.aggregate(max=models.Max('order'))['max'] or 0
    return max_order + 1


class PaymentMethod(models.Model):
    name = models.CharField(_("name"), max_length=50)
    method = models.CharField(_("method"), max_length=50, choices=PaymentMethods.choices, unique=True)
    logo = models.ImageField(_("logo"), upload_to="shop/payment_methods/", blank=True)
    enabled = models.BooleanField(
        _("enabled"), default=False,
        help_text=_("Whether the payment method can be used at checkout or not.")
    )
    order = models.PositiveSmallIntegerField(_("order"), default=get_max_order)

    class Meta:
        verbose_name = _("payment method")
        verbose_name_plural = _("payment methods")

    def __str__(self):
        return self.name
