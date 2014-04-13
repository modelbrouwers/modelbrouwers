from django.db import models
from django.utils.translation import ugettext as _


from general.models import OrderedUser
from datetime import datetime, timedelta

MINUTES_FOR_ONLINE = 5

class TrackedUser(models.Model):
    user = models.ForeignKey(OrderedUser, unique=True)
    last_seen = models.DateTimeField(_("last seen online"), auto_now=True)
    tracking_since = models.DateTimeField(auto_now_add=True)
    notificate = models.BooleanField(
            _("notificate"),
            default=True,
            help_text=_("Send a notification to the online "
                        "moderators when this user is online.")
        )

    class Meta:
        verbose_name = _("tracked user")
        verbose_name_plural = _("tracked users")
        ordering = ('-last_seen',)

    def __unicode__(self):
        return u"%s" % self.user.get_profile().forum_nickname

    @property
    def is_online(self):
        now = datetime.now()
        past = now - timedelta(minutes = MINUTES_FOR_ONLINE)
        if self.last_seen > past:
            return True
        return False
