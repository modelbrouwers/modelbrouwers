from django.conf import settings
from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from brouwers.general.utils import get_username


class Ban(models.Model):
    """Model to hold bans. Middleware grabs the bans from the database."""

    # TODO: lighten the load on the database: cache the bans, invalidate the
    # cache when bans are added, deleted or modified (on delete() and save())
    # Be carefull, queryset.delete() might not fire signals...

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_(u"user"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    ip = models.GenericIPAddressField(
        _(u"ip"), blank=True, null=True, help_text=_(u"Ip address to ban.")
    )
    expiry_date = models.DateTimeField(
        _(u"expiry date"),
        blank=True,
        null=True,
        help_text=_("Date the ban expires. Leave blank for permabans."),
    )
    reason_internal = models.TextField(_(u"reason (internal)"), blank=True)
    reason = models.TextField(
        _(u"reason"),
        blank=True,
        help_text=_(u"This reason will be shown to the banned user."),
    )
    automatic = models.BooleanField(_("automatically created?"), default=False)

    class Meta:
        verbose_name = _(u"ban")
        verbose_name_plural = _(u"bans")

    @property
    def expires(self):
        if not self.expiry_date:
            return _("never")
        return self.expiry_date

    @property
    def type(self):
        if not self.user:
            return _("ip ban")
        return _("account ban")

    def __str__(self):
        if self.user:
            return _("Ban: %(username)s") % {"username": get_username(self)}
        else:
            return _("Ban: %(ip)s") % {"ip": self.ip}

    def clean(self):
        super().clean()
        if not self.ip and not self.user:
            raise ValidationError(_("Submit either an user or IP address."))
        return self

    def save(self, *args, **kwargs):
        if not self.ip:
            self.ip = "0.0.0.0"  # bogus ip
        super().save(*args, **kwargs)

    @classmethod
    def get_bans_queryset(cls):
        q_date = Q(expiry_date__gte=timezone.now()) | Q(expiry_date=None)
        qs = cls.objects.filter(q_date)
        return qs
