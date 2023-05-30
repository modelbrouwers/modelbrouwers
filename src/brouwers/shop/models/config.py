from django.db import models
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel

__all__ = ["ShopConfiguration"]


class ShopConfiguration(SingletonModel):
    # Sisow
    sisow_test_mode = models.BooleanField(_("sisow test mode"), default=False)
    sisow_merchant_id = models.CharField(
        _("sisow merchant ID"), max_length=100, blank=True
    )
    sisow_merchant_key = models.CharField(
        _("sisow merchant key"), max_length=255, blank=True
    )

    # bank transfer
    bank_transfer_instructions = models.TextField(
        _("instructions"),
        help_text=_(
            "Enter the instructions to display to the customer on how to transfer the money."
        ),
    )

    # paypal
    paypal_sandbox = models.BooleanField(_("paypal sandbox"), default=True)
    paypal_client_id = models.CharField(
        _("paypal API client ID"), max_length=200, blank=True
    )
    paypal_secret = models.CharField(_("paypal API secret"), max_length=200, blank=True)

    # e-mails
    from_email = models.EmailField(
        _("from email"),
        blank=True,
        help_text=_(
            "Email address for outgoing e-mails. This will end up in the 'From' header - "
            "you must ensure that your outgoing email server is appropriately "
            "configured. If left blank, the default value from the settings is used."
        ),
    )

    class Meta:
        verbose_name = _("Shop configuration")

    def __str__(self):
        return "Shop configuration"
