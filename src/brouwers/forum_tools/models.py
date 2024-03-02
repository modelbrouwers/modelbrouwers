import zlib
from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta

from brouwers.general.utils import clean_username

from .fields import ForumToolsIDField


class ForumLinkBase(models.Model):
    link_id = models.CharField(
        _("link id"), max_length=128, help_text=_("HTML id of the base anchor.")
    )
    short_description = models.CharField(
        _("short description"), max_length=64, blank=True
    )
    enabled = models.BooleanField(
        _("enabled"), default=True, help_text=_("Enable the syncing of this link.")
    )
    from_date = models.DateField(
        _("from date"), help_text=_("Start date from when this link is enabled.")
    )
    to_date = models.DateField(
        _("to date"),
        help_text=_("End date from when this link is enabled, this date included."),
    )

    class Meta:
        verbose_name = _("base forum link")
        verbose_name_plural = _("base forum links")

    def __str__(self):
        if self.short_description:
            return _("base forum link: %(desc)s") % {"desc": self.short_description}
        else:
            return _("base forum link: %(id)s") % {"id": self.link_id}


class ForumLinkSynced(models.Model):
    base = models.ForeignKey(
        ForumLinkBase,
        verbose_name=_("base link"),
        help_text=_("Link this link syncs with."),
        on_delete=models.CASCADE,
    )
    link_id = models.CharField(
        _("link id"), max_length=128, help_text=_("HTML id of the anchor to be synced.")
    )

    class Meta:
        verbose_name = _("synced forum link")
        verbose_name_plural = _("synced forum links")

    def __str__(self):
        return "%s -- %s" % (self.base, self.link_id)


class BuildReportsForum(models.Model):
    """Model which tells us which forums hold build reports"""

    forum = ForumToolsIDField(_("forum"), type="forum")

    class Meta:
        verbose_name = _("build report forum")
        verbose_name_plural = _("build report forums")
        ordering = ["forum"]

    def __str__(self):
        return self.forum.forum_name if self.forum else _("(forum does not exist)")


class ForumCategory(models.Model):
    name = models.CharField(_("name"), max_length=255)
    forum = ForumToolsIDField(_("forum"), type="forum", blank=True, null=True)
    icon_class = models.CharField(_("icon class"), max_length=50, blank=True)

    class Meta:
        verbose_name = _("forum category")
        verbose_name_plural = _("forum categories")
        ordering = ("name",)

    def __str__(self):
        return self.name


# Models to interact with the MYSQL database #############################


class ForumUser(models.Model):
    """MySQL phpBB3 user, managed by phpBB3"""

    # mediumint(8) unsigned
    user_id = models.AutoField(primary_key=True, help_text=_("Primary key"))
    username = models.CharField(_("username"), max_length=255)
    username_clean = models.CharField(_("username"), max_length=255)
    user_posts = models.IntegerField()
    user_email = models.CharField(_("email"), max_length=100)
    # bigint(20)
    user_email_hash = models.BigIntegerField(
        db_column="user_email_hash",
        default=0,
        help_text=_("A hash of the user's email address."),
    )
    user_permissions = models.TextField(blank=True)
    user_sig = models.TextField(blank=True)
    user_interests = models.TextField(blank=True)
    user_actkey = models.TextField(blank=True)
    user_occ = models.TextField(blank=True)

    class Meta:
        managed = False
        verbose_name = _("forum user")
        verbose_name_plural = _("forum users")
        ordering = ("username",)
        db_table = "%susers" % settings.PHPBB_TABLE_PREFIX

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        qs = {
            "mode": "viewprofile",
            "u": self.user_id,
        }
        return "{0}?{1}".format(reverse("phpBB:memberlist"), urlencode(qs))

    def get_email_hash(self):
        email = self.user_email
        h = zlib.crc32(email.lower().encode("ascii")) & 0xFFFFFFFF
        return "%s%s" % (h, len(email))

    def save(self, *args, **kwargs):
        self.user_email_hash = self.get_email_hash()
        if not self.username_clean:
            self._clean_username()
        super().save(*args, **kwargs)

    def _clean_username(self):
        self.username_clean = clean_username(self.username)


class Forum(models.Model):
    """
    MySQL Forum, managed by phpBB3
    """

    forum_id = models.AutoField(primary_key=True)
    forum_name = models.CharField(max_length=60)
    forum_topics = models.IntegerField(default=0)
    forum_posts = models.IntegerField(default=0)
    forum_desc = models.TextField()
    parent = models.ForeignKey(
        "self",
        related_name="child",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.forum_name

    def get_absolute_url(self):
        qs = {"f": self.forum_id}
        return "{0}?{1}".format(reverse("phpBB:viewforum"), urlencode(qs))

    class Meta:
        managed = False
        db_table = settings.PHPBB_TABLE_PREFIX + "forums"
        ordering = ["forum_name"]


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    topic_title = models.CharField(max_length=255)
    last_post_time = models.BigIntegerField(db_column="topic_last_post_time", default=0)
    create_time = models.BigIntegerField(db_column="topic_time", default=0)

    author = models.ForeignKey(
        ForumUser,
        db_column="topic_poster",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        managed = False
        db_table = settings.PHPBB_TABLE_PREFIX + "topics"
        ordering = ["topic_id"]

    def __str__(self):
        return self.topic_title

    def get_absolute_url(self):
        qs = {"t": self.topic_id}
        if self.forum.pk:
            qs["f"] = self.forum.pk
        return "{0}?{1}".format(reverse("phpBB:viewtopic"), urlencode(qs))

    @property
    def created(self):
        return datetime.utcfromtimestamp(self.create_time).replace(tzinfo=timezone.utc)

    def get_last_post_time(self):
        return datetime.utcfromtimestamp(self.last_post_time).replace(
            tzinfo=timezone.utc
        )

    @property
    def is_dead(self):
        """
        If the last post is older than settings.TOPIC_DEAD_TIME, it's considered
        dead.
        """
        last = self.get_last_post_time()
        lower = timezone.now() - relativedelta(months=settings.TOPIC_DEAD_TIME)
        return last <= lower

    @property
    def age(self):
        return timesince(self.get_last_post_time())

    @property
    def text_dead(self):
        return _(
            "This topic has been inactive for: {0}. Please consider "
            "sending the author a private message instead of replying "
            "and thus bumping the topic."
        ).format(self.age)


class ForumPostCountRestriction(models.Model):
    """Model to hold information on the minimum post-count and level of posting rights.
    Managed by Django."""

    POSTING_LEVELS = (
        ("T", _("Topic")),
        ("R", _("Reply")),
    )

    forum = ForumToolsIDField(_("forum id"), type="forum", blank=True, null=True)
    min_posts = models.PositiveSmallIntegerField(_("minimum number of posts"))
    posting_level = models.CharField(
        _("posting level"), max_length=1, choices=POSTING_LEVELS
    )

    class Meta:
        verbose_name = _("forum post count restriction")
        verbose_name_plural = _("forum post count restrictions")
        ordering = ["forum"]

    def __str__(self):
        return _("Restriction for %(forum)s") % {"forum": self.forum.forum_name}


class Report(models.Model):
    """MySQL Report model, managed by phpBB3"""

    report_id = models.AutoField(primary_key=True, help_text="Primary key")
    # reason_id = FK to reasons, not implement in Django yet
    report_closed = models.BooleanField(
        _("closed"),
        default=False,
        help_text=_("Closed reports need no more attention."),
    )
    report_time_int = models.IntegerField(
        _("time"),
        db_column="report_time",
        help_text=_("UNIX time when the report was added."),
    )
    report_text = models.TextField("text", blank=True)

    class Meta:
        managed = False
        verbose_name = _("report")
        verbose_name_plural = _("reports")
        db_table = "%sreports" % settings.PHPBB_TABLE_PREFIX
        permissions = (("can_see_reports", _("Can see (number of) open reports")),)

    def __str__(self):
        return _("Report %(id)s" % {"id": self.report_id})

    def report_time(self):
        return datetime.fromtimestamp(self.report_time_int)
