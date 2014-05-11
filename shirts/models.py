from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

BASE_PRICE = 10.0
SHIPPING_COST = 3.20

class ShirtOrder(models.Model):
    SIZES = (
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("XXXL", "XXXL"),
    )
    TYPES = (
        ("S", _("Standard")),
        ("G", _("Girlie")),
    )
    COLORS = (
        ("W", _("White")),
        ("B", _("Black"))
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    size = models.CharField(_("size"), max_length=4, choices=SIZES, default="L")
    type = models.CharField(_("type"), max_length=1, choices=TYPES, default="S")
    color = models.CharField(_("color"), max_length=2, choices=COLORS, default="W")
    send_per_mail = models.BooleanField(_("mail the shirt"), help_text=_("Mailing the shirt will add %(shipping_cost)s euros to the costs and you need to fill in your address data in your profile.") % {'shipping_cost': SHIPPING_COST})
    moderator = models.BooleanField(_("moderator shirt"), help_text=_("Check this box if you want the moderator shirt. Moderators only!"))

    #internal
    order_time = models.DateTimeField(_("order time"), auto_now_add=True)
    payment_received = models.BooleanField(_("payment received"))
    delivered = models.BooleanField(_("delivered?"))

    class Meta:
        verbose_name = _("shirt order")
        verbose_name_plural = _("shirt orders")
        ordering = ('order_time',)

    @property
    def price(self):
        price = BASE_PRICE # in euros
        if self.send_per_mail:
            price += SHIPPING_COST
        return price

    @property
    def user_email(self):
        return self.user.email
