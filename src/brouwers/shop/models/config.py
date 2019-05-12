from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from solo.models import SingletonModel


@python_2_unicode_compatible
class ShopConfiguration(SingletonModel):

    sisow_test_mode = models.BooleanField(_("sisow test mode"), default=False)
    sisow_merchant_id = models.CharField(_("sisow merchant ID"), max_length=100, blank=True)
    sisow_merchant_key = models.CharField(_("sisow merchant key"), max_length=255, blank=True)

    class Meta:
        verbose_name = _("Shop configuration")

    def __str__(self):
        return "Shop configuration"
