import warnings
from datetime import datetime
import zlib

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from general.utils import clean_username


class ForumMixin(object):
    """ Depcreated """

    def __init__(self, *args, **kwargs):
        super(ForumMixin, self).__init__(*args, **kwargs)
        warnings.warn("brouwers.forum_tools.models.ForumMixin is deprecated, "
                      "use brouwers.forum_tools.fields.ForumToolsIDField instead",
              DeprecationWarning)

    @cached_property
    def forum(self):
        try:
            return Forum.objects.get(pk=self.forum_id)
        except Forum.DoesNotExist:
            return None

    @property
    def forum_name(self):
        return self.forum.forum_name


class ForumLinkBase(models.Model):
    link_id = models.CharField(_('link id'), max_length=128, help_text=_('HTML id of the base anchor.'))
    short_description = models.CharField(_('short description'), max_length=64, blank=True)
    enabled = models.BooleanField(
                _('enabled'), default=True,
                help_text=_('Enable the syncing of this link.')
                )
    from_date = models.DateField(_('from date'), help_text=_('Start date from when this link is enabled.'))
    to_date = models.DateField(_('to date'), help_text=_('End date from when this link is enabled, this date included.'))

    class Meta:
        verbose_name = _('base forum link')
        verbose_name_plural = _('base forum links')

    def __unicode__(self):
        if self.short_description:
            return _(u'base forum link: %(desc)s') % {'desc': self.short_description}
        else:
            return _(u'base forum link: %(id)s') % {'id': self.link_id}

class ForumLinkSynced(models.Model):
    base = models.ForeignKey(ForumLinkBase, verbose_name=_('base link'), help_text=_('Link this link syncs with.'))
    link_id = models.CharField(_('link id'), max_length=128, help_text=_('HTML id of the anchor to be synced.'))

    class Meta:
        verbose_name = _('synced forum link')
        verbose_name_plural = _('synced forum links')

    def __unicode__(self):
        return u"%s -- %s" % (self.base.__unicode__(), self.link_id)


class BuildReportsForum(ForumMixin, models.Model):
    """ Model which tells us which forums hold build reports """
    forum_id = models.PositiveIntegerField()

    class Meta:
        verbose_name = _(u'build report forum')
        verbose_name_plural = _(u'build report forums')
        ordering = ['forum_id']

    def __unicode__(self):
        return self.forum_name


class ForumCategory(ForumMixin, models.Model):
    name = models.CharField(_('name'), max_length=255)
    forum_id = models.PositiveIntegerField(_('phpBB forum id'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'forum category')
        verbose_name_plural = _(u'forum categories')
        ordering = ('name',)

    def __unicode__(self):
        return self.name


########## Models to interact with the MYSQL database #############################


class ForumUser(models.Model):
    """ MySQL phpBB3 user, managed by phpBB3 """
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text=_("Primary key")
    )
    username = models.CharField(_("username"), max_length=255)
    username_clean = models.CharField(_("username"), max_length=255)
    user_posts = models.IntegerField()
    user_email = models.CharField(_("email"), max_length=100)
    user_email_hash = models.BigIntegerField(db_column="user_email_hash",
        # bigint(20)
        default=0,
        help_text=_("A hash of the user's email address.")
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
        ordering = ('username',)
        db_table = u"%susers" % settings.PHPBB_TABLE_PREFIX

    def __unicode__(self):
        return u"%s" % self.username

    def get_absolute_url(self):
        return "%s/memberlist.php?mode=viewprofile&u=%s" % (settings.PHPBB_URL, self.user_id)

    def get_email_hash(self):
        email = self.user_email
        h = zlib.crc32(email.lower()) & 0xffffffff
        return "%s%s" % (h, len(email))

    def save(self, *args, **kwargs):
        self.user_email_hash = self.get_email_hash()
        if not self.username_clean:
            self._clean_username()
        super(ForumUser, self).save(*args, **kwargs)

    def _clean_username(self):
        self.username_clean = clean_username(self.username)


class Forum(models.Model):
    """ MySQL Forum, managed by phpBB3 """
    forum_id = models.IntegerField(primary_key=True)
    forum_name = models.CharField(max_length=60)
    forum_topics = models.IntegerField(default=0)
    forum_posts = models.IntegerField(default=0)
    # forum_last_post = models.OneToOneField(
    #         'PhpbbPost',
    #         db_column='forum_last_post_id',
    #         related_name="last_post_of_forum")
    forum_desc = models.TextField()
    parent = models.ForeignKey('self', related_name="child", default=0)
    # left = models.OneToOneField('self', related_name="right_of")
    # right = models.OneToOneField('self', related_name="left_of")

    def __unicode__(self):
        return u"%s" % self.forum_name

    def get_absolute_url(self):
        return "{prefix}/viewforum.php?f={id}".format(prefix=settings.PHPBB_URL, id=self.forum_id)

    # def get_slug(self):
    #     return slugify(self.forum_name)

    class Meta:
        managed = False
        db_table = settings.PHPBB_TABLE_PREFIX + 'forums'
        ordering = ['forum_name']


class Topic(models.Model):
    topic_id = models.IntegerField(primary_key=True)
    forum = models.ForeignKey(Forum)
    topic_title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = settings.PHPBB_TABLE_PREFIX + 'topics'
        ordering = ['topic_id']


class ForumPostCountRestriction(models.Model):
    """ Model to hold information on the minimum post-count and level of posting rights.
        Managed by Django. """

    POSTING_LEVELS = (
        ('T', _('Topic')),
        ('R', _('Reply')),
        )

    forum = models.ForeignKey(Forum)
    min_posts = models.PositiveSmallIntegerField(_('minimum number of posts'))
    posting_level = models.CharField(_('posting level'), max_length=1,
                    choices=POSTING_LEVELS
                )

    class Meta:
        verbose_name = _('forum post count restriction')
        verbose_name_plural = _('forum post count restrictions')
        ordering = ['forum']

    def __unicode__(self):
        return _("Restriction for %(forum)s") % {'forum': self.forum.forum_name}


class Report(models.Model):
    """ MySQL Report model, managed by phpBB3 """
    report_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="Primary key"
    )
    #reason_id = FK to reasons, not implement in Django yet
    report_closed = models.BooleanField(_('closed'), help_text=_('Closed reports need no more attention.'))
    report_time_int = models.IntegerField(_('time'), db_column="report_time", help_text=_('UNIX time when the report was added.'))
    report_text = models.TextField('text', blank=True)

    class Meta:
        managed = False
        verbose_name = _('report')
        verbose_name_plural = _('reports')
        db_table = u"%sreports" % settings.PHPBB_TABLE_PREFIX
        permissions = (
            ("can_see_reports", _("Can see (number of) open reports")),
        )

    def __unicode__(self):
        return _('Report %(id)s' % {'id': self.report_id})

    def report_time(self):
        return datetime.fromtimestamp(self.report_time_int)
