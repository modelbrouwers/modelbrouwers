from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

MINUTES_FOR_ONLINE = 5


class TrackedUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.user.username

    @property
    def is_online(self):
        now = timezone.now()
        past = now - timedelta(minutes=MINUTES_FOR_ONLINE)
        if self.last_seen > past:
            return True
        return False
