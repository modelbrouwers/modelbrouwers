from datetime import timedelta
import calendar

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djchoices import DjangoChoices, ChoiceItem
from autoslug import AutoSlugField

from forum_tools.models import ForumCategory, ForumMixin
from forum_tools.fields import ForumToolsIDField
from .managers import PublicGroupBuildsManager


class GroupbuildDurations(DjangoChoices):
    one_month = ChoiceItem(30, _('30 days'))
    two_months = ChoiceItem(61, _('2 months'))
    three_months = ChoiceItem(92, _('3 months'))
    six_months = ChoiceItem(183, _('6 months'))
    twelve_months = ChoiceItem(365, ('one year'))


class GroupbuildStatuses(DjangoChoices):
    concept = ChoiceItem('concept', _('concept/idea'))
    submitted = ChoiceItem('submitted', _('submitted'))
    accepted = ChoiceItem('accepted', _('accepted'))
    denied = ChoiceItem('denied', _('denied'))
    extended = ChoiceItem('extended', _('extended'))

# public statuses
date_bound_statuses = [GroupbuildStatuses.accepted, GroupbuildStatuses.extended]
non_date_bound_statuses = [GroupbuildStatuses.concept, GroupbuildStatuses.submitted]

GroupbuildStatuses.date_bound_statuses = date_bound_statuses
GroupbuildStatuses.non_date_bound_statuses = non_date_bound_statuses
GroupbuildStatuses.public_statuses = non_date_bound_statuses + date_bound_statuses


class GroupBuild(ForumMixin, models.Model):
    forum_id = ForumToolsIDField(_('forum id'), type='forum', blank=True, null=True,
        help_text=_('Forum id of the group build subforum'))

    # core information
    theme = models.CharField(_('theme'), max_length=100,
                             help_text=_('Theme/name of the group build'))
    slug = AutoSlugField(_('slug'), editable=True, unique=True, populate_from='theme')

    category = models.ForeignKey(
        ForumCategory, verbose_name=_('forum category'))
    description = models.TextField(
        _('description'), help_text=_('Short description'))
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_('admins'),
        help_text=_('Users who manage the group build.'), related_name='admin_groupbuilds',
        limit_choices_to={'is_active': True})  # role maybe with through table

    start = models.DateField(_('start date'), blank=True, null=True,
                             help_text=_('Date when you want to start building.'))
    end = models.DateField(_('end date'), blank=True, null=True,
                           help_text=_('Date this build ends.'))
    duration = models.PositiveSmallIntegerField(_('duration'),
                                                choices=GroupbuildDurations.choices, default=GroupbuildDurations.three_months)

    # motivation, approval, voting popularity...
    status = models.CharField(_('status'), max_length=10,
                              choices=GroupbuildStatuses.choices, default=GroupbuildStatuses.concept)
    users_can_vote = models.BooleanField(_('users can vote'), default=False,
                                         help_text=_('Let users vote to determine the build popularity'))
    upvotes = models.PositiveSmallIntegerField(
        _('upvotes'), blank=True, null=True)
    downvotes = models.PositiveSmallIntegerField(
        _('downvotes'), blank=True, null=True)

    # participants management
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, null=True,
        through='Participant', related_name='groupbuilds')

    # optional 'experience enhancing' fields
    rules = models.TextField(blank=True)
    rules_topic_id = ForumToolsIDField(_('rules topic'), blank=True, null=True, type='topic')
    homepage_topic_id = ForumToolsIDField(_('topic to direct to from calendar'),
        blank=True, null=True, type='topic')
    introduction_topic_id = ForumToolsIDField(_('introduction topic'),
        blank=True, null=True, type='topic')

    # logging
    # pretty much the owner
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='groupbuilds_applied')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    reason_denied = models.TextField(blank=True)

    # TODO: status tracking -> forum created, forum visible etc...

    objects = models.Manager()
    public = PublicGroupBuildsManager()

    _created = False
    _dimensions = None

    class Meta:
        verbose_name = _(u'group build')
        verbose_name_plural = _(u'group builds')
        ordering = ('-modified', '-created')  # most recently changed first

    def save(self, *args, **kwargs):
        if self.start and not self.end:
            self.end = self.start + timedelta(days=self.duration)
        if not self.id:
            self._created = True
        super(GroupBuild, self).save(*args, **kwargs)

    def __unicode__(self):
        return _("{name}: {status}").format(name=self.theme, status=self.get_status_display())

    def get_absolute_url(self):
        return reverse('groupbuilds:detail', kwargs={'slug': self.slug})

    def num_participants(self):
        return self.participants.count()
    num_participants.short_description = _('# participants')

    def set_calendar_dimensions(self, start, end, num_months=6):
        # number of months
        days_last_month = calendar.monthrange(self.end.year, self.end.month)[1]
        days_first_month = calendar.monthrange(self.start.year, self.start.month)[1]

        n_months = (self.end.year - self.start.year) * 12 + self.end.month - self.start.month + 1
        n_full_months = n_months
        if self.start.day != 1:
            n_full_months -= 1
        if self.end.day != days_last_month:
            n_full_months -= 1

        # percentages
        offset_start = ((self.start.day-1) / float(days_first_month) + (self.start.month - start.month)) / float(num_months)
        pct_last_month = self.end.day / float(days_last_month)
        pct_first_month = 1-(offset_start) if n_months > 1 else pct_last_month

        # calculated width
        if n_months < 2:
            pct_last_month = 0.0

        width = (pct_first_month + pct_last_month + max(n_months - 2, 0)) / float(num_months)
        if offset_start < 0:
            width += offset_start
            offset_start = 0.0

        self._dimensions = {
            'offset': offset_start * 100,
            'width': min(width, 1.0) * 100,
        }

    @property
    def calendar_dimensions(self):
        return self._dimensions


class Participant(models.Model):
    groupbuild = models.ForeignKey(GroupBuild)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='gb_participants')
    model_name = models.CharField(_('model name'), max_length=255, blank=True)

    finished = models.BooleanField(_('finished'), default=False)
    topic_id = models.PositiveIntegerField(_('topic'), blank=True, null=True)

    # competition element
    points = models.SmallIntegerField(_('points'), blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(u'group build participant')
        verbose_name_plural = _(u'group build participants')

    def __unicode__(self):
        return _("{build} participant: {user}").format(
            build=self.groupbuild.theme,
            user=self.user.username
        )
