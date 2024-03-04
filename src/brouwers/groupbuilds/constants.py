from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupbuildStatuses(models.TextChoices):
    concept = "concept", _("concept/idea")
    submitted = "submitted", _("submitted for review")
    accepted = "accepted", _("accepted")
    denied = "denied", _("denied")
    extended = "extended", _("extended")
