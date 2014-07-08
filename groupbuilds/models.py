from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djchoices import DjangoChoices, ChoiceItem
from autoslug import AutoSlugField

from forum_tools.models import ForumCategory, ForumMixin
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

GroupbuildStatuses.public_statuses = [GroupbuildStatuses.concept,
                                      GroupbuildStatuses.submitted,
                                      GroupbuildStatuses.accepted,
                                      GroupbuildStatuses.extended]


class GroupBuild(ForumMixin, models.Model):
    forum_id = models.PositiveIntegerField(
        _('forum id'), blank=True, null=True,
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
        help_text=_('Users who manage the group build.'), related_name='admin_groupbuilds')  # role maybe with through table

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
    rules_topic_id = models.PositiveIntegerField(
        _('rules topic'), blank=True, null=True)
    homepage_topic_id = models.PositiveIntegerField(
        _('topic to direct to from calendar'), blank=True, null=True)
    introduction_topic_id = models.PositiveIntegerField(
        _('introduction topic'), blank=True, null=True)

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

    class Meta:
        verbose_name = _(u'group build')
        verbose_name_plural = _(u'group builds')
        ordering = ('-modified', '-created')  # most recently changed first

    def __unicode__(self):
        return _("{name}: {status}").format(name=self.theme, status=self.get_status_display())

    def num_participants(self):
        return self.participants.count()
    num_participants.short_description = _('# participants')


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
