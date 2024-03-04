from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField
from precise_bbcode.shortcuts import render_bbcodes

from brouwers.forum_tools.fields import ForumToolsIDField
from brouwers.forum_tools.models import ForumCategory

from .constants import GroupbuildStatuses


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

    start = models.DateField(
        _("start date"),
        blank=True,
        null=True,
        help_text=_("Date when you want to start building."),
    )
    end = models.DateField(
        _("end date"), blank=True, null=True, help_text=_("Date this build ends.")
    )

    # motivation, approval, voting popularity...
    status = models.CharField(
        _("status"),
        max_length=10,
        choices=GroupbuildStatuses.choices,
        default=GroupbuildStatuses.concept,
    )

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

    class Meta:
        verbose_name = _("group build")
        verbose_name_plural = _("group builds")
        ordering = ("-modified", "-created")  # most recently changed first

    def __str__(self):
        return _("{name}: {status}").format(
            name=self.theme, status=self.get_status_display()
        )

    def get_absolute_url(self):
        return reverse("groupbuilds:detail", kwargs={"slug": self.slug})

    @property
    def has_links(self):
        return (
            self.forum
            or self.introduction_topic
            or self.homepage_topic
            or self.rules_topic
        )

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

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("group build participant")
        verbose_name_plural = _("group build participants")

    def __str__(self):
        return _("{build} participant: {user}").format(
            build=self.groupbuild.theme, user=self.user.username
        )
