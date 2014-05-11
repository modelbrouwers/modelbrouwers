from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from general.utils import get_username


class Ban(models.Model):
    """ Model to hold bans. Middleware grabs the bans from the database. """
    # TODO: lighten the load on the database: cache the bans, invalidate the
    # cache when bans are added, deleted or modified (on delete() and save())
    # Be carefull, queryset.delete() might not fire signals...

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'user'), blank=True, null=True)
    ip = models.IPAddressField(
        _(u'ip'),
        help_text = _(u'Ip address to ban.'),
        blank = True
        )
    expiry_date = models.DateTimeField(
        _(u'expiry date'),
        blank = True, null = True,
        help_text = _('Date the ban expires. Leave blank for permabans.')
        )
    reason_internal = models.TextField(_(u'reason (internal)'), blank=True)
    reason = models.TextField(
        _(u'reason'), blank=True,
        help_text=_(u'This reason will be shown to the banned user.')
        )
    automatic = models.BooleanField(_('automatically created?'), default=False)

    class Meta:
        verbose_name = _(u'ban')
        verbose_name_plural = _(u'bans')

    @property
    def expires(self):
        if not self.expiry_date:
            return _('never')
        return self.expiry_date

    @property
    def type(self):
        if not self.user:
            return _('ip ban')
        return _('account ban')

    def __unicode__(self):
        if self.user:
            return _(u'Ban: %(username)s')  % {'username': get_username(self)}
        else:
            return _(u'Ban: %(ip)s') % {'ip': self.ip}

    def clean(self):
        super(Ban, self).clean()
        if not self.ip and not self.user:
            raise ValidationError(_(u'Submit either an user or IP address.'))
        return self

    def save(self, *args, **kwargs):
        if not self.ip:
            self.ip = '0.0.0.0' # bogus ip
        super(Ban, self).save(*args, **kwargs)

    @classmethod
    def get_bans_queryset(cls):
        q_date = Q(expiry_date__gte=datetime.now()) | Q(expiry_date=None)
        qs = cls.objects.filter(q_date)
        return qs