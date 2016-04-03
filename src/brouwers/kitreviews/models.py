from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem

from brouwers.albums.models import Album
from brouwers.general.utils import get_username

RATING_BASE = 100  # store ratings relative to 100
RATING_DISPLAY_BASE = 5
DEFAULT_RATING = 50
DEFAULT_DIFFICULTY = 3
MAX_RATING = 100
MIN_RATING = 0


class KitReview(models.Model):
    """ Model holding the review information for a model kit """

    model_kit = models.ForeignKey('kits.ModelKit')
    raw_text = models.TextField(
        _(u'review'),
        help_text=_('This is your review. You can use BBCode here.')
    )
    html = models.TextField(blank=True, help_text=u'raw_text with BBCode rendered as html')
    prop = models.ManyToManyField('KitReviewProperty', blank=True, related_name='reviews')
    rating = models.PositiveSmallIntegerField(_(u'rating'), default=DEFAULT_RATING,
                                              validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)])

    # linking to extra information
    album = models.ForeignKey(Album, verbose_name=_('album'), blank=True, null=True)
    topic_id = models.PositiveIntegerField(
        _('topic'), blank=True,
        null=True, help_text=_('ID of the topic on Modelbrouwers.')
    )
    external_topic_url = models.URLField(
        _('topic url'), blank=True,
        help_text=_('URL to the topic not hosted on Modelbrouwers')
    )

    # some privacy settings...
    show_real_name = models.BooleanField(
        _('show real name?'), default=True,
        help_text=_('Checking this option will display your real name as reviewer. Uncheck to use your nickname.'),
    )

    # internal information
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL)
    submitted_on = models.DateTimeField(auto_now_add=True)
    last_edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _(u'kit review')
        verbose_name_plural = _(u'kit reviews')

    def __unicode__(self):
        return _(u'Review: %(kit)s by %(user)s') % {
            'kit': self.model_kit.name,
            'user': get_username(self, field='reviewer'),
        }

    @property
    def votes(self):
        votes_pos = self.kitreviewvote_set.filter(vote='+').count()
        votes_neg = self.kitreviewvote_set.filter(vote='-').count()
        votes_total = votes_pos + votes_neg
        return (votes_pos, votes_neg, votes_total)

    @property
    def topic_url(self):
        if self.topic_id:
            domain = Site.objects.get_current().domain
            topic_url = "%(http)s%(domain)s%(phpBB)s%(topic)s" % {
                'http': 'http://',  # TODO: check for https or http
                'domain': domain,
                'phpBB': settings.PHPBB_URL,
                'topic': '/viewtopic.php?t=%d' % self.topic_id
            }
            return topic_url
        elif self.external_topic_url:
            return self.external_topic_url
        return None


class KitReviewVote(models.Model):
    """ Model holding the votes for kitreviews, showing the quality of the review """

    VOTE_TYPES = (
        ('+', '+'),
        ('-', '-'),
    )

    kit_review = models.ForeignKey(KitReview)
    vote = models.CharField(_('vote'), max_length=1, db_index=True)
    voter = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = _(u'kit review vote')
        verbose_name_plural = _(u'kit review votes')
        unique_together = (('kit_review', 'voter'),)

    def __unicode__(self):
        return _(u"Vote for review by %(review_submitter)s") % {
            'review_submitter': get_username(self.kit_review, field='reviewer')
        }


class KitReviewProperty(models.Model):
    """ Model containing the properties of a review, which based on their score are divided into pros and cons"""

    name = models.CharField(_(u'name'), max_length=255)
    rating = models.PositiveSmallIntegerField(_(u'rating'), default=DEFAULT_RATING,
                                              validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)])

    class Meta:
        verbose_name = _(u'kit review property')
        verbose_name_plural = _(u'kit review properties')

    def __unicode__(self):
        return _(u'%(name)s: %(rating)s') % {
            'name': self.name,
            'rating': self.rating
        }
