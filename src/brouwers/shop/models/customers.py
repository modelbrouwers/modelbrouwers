from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomerGroup(models.Model):
    name = models.CharField(_("name"), max_length=200)
    discount = models.DecimalField(
        _("discount"), max_digits=3, decimal_places=2, default=0
    )

    class Meta:
        verbose_name = _("customer group")
        verbose_name_plural = _("customer groups")

    def __str__(self):
        return self.name
