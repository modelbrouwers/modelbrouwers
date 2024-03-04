import calendar
from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import bleach
from autoslug import AutoSlugField
from precise_bbcode.shortcuts import render_bbcodes

from brouwers.forum_tools.fields import ForumToolsIDField
from brouwers.forum_tools.models import ForumCategory

from .constants import GroupbuildDurations, GroupbuildStatuses


class GroupBuild(models.Model):
    forum = ForumToolsIDField(
        _("forum id"),
        type="forum",
        blank=True,
        null=True,
        help_text=_("Forum id of the group build subforum"),
    )

    # core information
    theme = models.CharField(
        _("theme"), max_length=100, help_text=_("Theme/name of the group build")
    )
    slug = AutoSlugField(_("slug"), editable=True, unique=True, populate_from="theme")

    category = models.ForeignKey(
        ForumCategory, verbose_name=_("forum category"), on_delete=models.CASCADE
    )
    description = models.TextField(_("description"), help_text=_("Short description"))
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("admins"),
        help_text=_("Users who manage the group build."),
        related_name="admin_groupbuilds",
        limit_choices_to={"is_active": True},
    )  # role maybe with through table

    start = models.DateField(
        _("start date"),
        blank=True,
        null=True,
        help_text=_("Date when you want to start building."),
    )
    end = models.DateField(
        _("end date"), blank=True, null=True, help_text=_("Date this build ends.")
    )
    duration = models.PositiveSmallIntegerField(
        _("duration"),
        choices=GroupbuildDurations.choices,
        default=GroupbuildDurations.three_months,
    )

    # motivation, approval, voting popularity...
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=GroupbuildStatuses.choices,
        default=GroupbuildStatuses.concept,
    )
    users_can_vote = models.BooleanField(
        _("users can vote"),
        default=False,
        help_text=_("Let users vote to determine the build popularity"),
    )
    upvotes = models.PositiveSmallIntegerField(_("upvotes"), blank=True, null=True)
    downvotes = models.PositiveSmallIntegerField(_("downvotes"), blank=True, null=True)

    # participants management
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        through="Participant",
        related_name="groupbuilds",
    )

    # optional 'experience enhancing' fields
    rules = models.TextField(blank=True)
    rules_topic = ForumToolsIDField(
        _("rules topic"), blank=True, null=True, type="topic"
    )
    homepage_topic = ForumToolsIDField(
        _("topic to direct to from calendar"), blank=True, null=True, type="topic"
    )
    introduction_topic = ForumToolsIDField(
        _("introduction topic"), blank=True, null=True, type="topic"
    )

    # logging
    # pretty much the owner
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="groupbuilds_applied",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    reason_denied = models.TextField(blank=True)

    _created = False
    _dimensions = None

    class Meta:
        verbose_name = _("group build")
        verbose_name_plural = _("group builds")
        ordering = ("-modified", "-created")  # most recently changed first

    def save(self, *args, **kwargs):
        if self.start and not self.end:
            self.end = self.start + timedelta(days=self.duration)
        if not self.id:
            self._created = True
        super().save(*args, **kwargs)

    def __str__(self):
        return _("{name}: {status}").format(
            name=self.theme, status=self.get_status_display()
        )

    def get_absolute_url(self):
        return reverse("groupbuilds:detail", kwargs={"slug": self.slug})

    def clean(self):
        self.rules = bleach.clean(self.rules)
        self.description = bleach.clean(self.description)

    def num_participants(self):
        return self.participants.count()

    num_participants.short_description = _("# participants")

    def set_calendar_dimensions(self, start, end, num_months=6):
        num_months = float(num_months)
        # number of months
        days_first_month = float(
            calendar.monthrange(self.start.year, self.start.month)[1]
        )
        days_last_month = float(calendar.monthrange(self.end.year, self.end.month)[1])

        # calculate the offset
        if self.start <= start:
            offset = 0.0
        else:
            # check the number of months difference
            diff_months = (self.start.month - start.month) + 12 * (
                self.start.year - start.year
            )
            # calculate in the started month percentage
            ratio_days = (self.start.day - 1) / days_first_month
            offset = (diff_months + ratio_days) / num_months

        # calculate the width
        if self.end >= end:
            width = 1.0 - offset
        else:
            # check number of months until end
            diff_years = 12 * (self.end.year - self.start.year)
            duration_gb = self.end.month - self.start.month + diff_years
            duration_left = (
                12 * (self.end.year - start.year) + self.end.month - start.month
            )
            diff_months = min(duration_left, duration_gb)
            # calculate in the percentage of the last month
            ratio_days1 = (self.start.day - 1) / days_first_month
            ratio_days2 = self.end.day / days_last_month
            width = (diff_months + ratio_days2 - ratio_days1) / num_months

        self._dimensions = {
            "offset": offset * 100,
            "width": width * 100,
        }

    @property
    def calendar_dimensions(self):
        return self._dimensions

    @property
    def has_links(self):
        return (
            self.forum
            or self.introduction_topic
            or self.homepage_topic
            or self.rules_topic
        )

    @property
    def is_ongoing(self):
        if not hasattr(self, "_is_ongoing"):
            now = timezone.now().date()
            self._is_ongoing = self.start and self.end and self.start <= now <= self.end
        return self._is_ongoing

    @property
    def is_open(self):
        now = timezone.now().date()
        if self.status == GroupbuildStatuses.denied:
            return False
        if self.end and self.end <= now:  # ended
            return False
        return True

    @property
    def is_submittable(self):
        has_dates = self.start is not None and self.end is not None
        return has_dates and self.status == GroupbuildStatuses.concept

    @property
    def progress(self):
        if not self.is_ongoing:
            return 0

        if not hasattr(self, "_progress"):
            today = date.today()
            total_delta = (self.end - self.start) or 1
            delta = today - self.start
            self._progress = float(delta.days) / total_delta.days
        return self._progress

    def get_field_rendered(self, field) -> str:
        return render_bbcodes(getattr(self, field))

    def get_description_rendered(self) -> str:
        return self.get_field_rendered("description")

    def get_rules_rendered(self) -> str:
        return self.get_field_rendered("rules")


class Participant(models.Model):
    groupbuild = models.ForeignKey(GroupBuild, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="gb_participants",
        on_delete=models.CASCADE,
    )
    model_name = models.CharField(_("model name"), max_length=255, blank=True)

    finished = models.BooleanField(_("finished"), default=False)
    topic = ForumToolsIDField(_("topic"), blank=True, null=True, type="topic")

    # competition element
    points = models.SmallIntegerField(_("points"), blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("group build participant")
        verbose_name_plural = _("group build participants")

    def __str__(self):
        return _("{build} participant: {user}").format(
            build=self.groupbuild.theme, user=self.user.username
        )
