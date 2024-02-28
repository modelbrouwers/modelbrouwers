from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupbuildDurations(models.IntegerChoices):
    one_month = 30, _("30 days")
    two_months = 61, _("2 months")
    three_months = 92, _("3 months")
    six_months = 183, _("6 months")
    twelve_months = 365, _("one year")


class GroupbuildStatuses(models.TextChoices):
    concept = "concept", _("concept/idea")
    submitted = "submitted", _("submitted for review")
    accepted = "accepted", _("accepted")
    denied = "denied", _("denied")
    extended = "extended", _("extended")


DATE_BOUND_STATUSES = [GroupbuildStatuses.accepted, GroupbuildStatuses.extended]
NON_DATE_BOUND_STATUSES = [GroupbuildStatuses.concept, GroupbuildStatuses.submitted]
PUBLIC_STATUSES = NON_DATE_BOUND_STATUSES + DATE_BOUND_STATUSES
