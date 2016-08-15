from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

from brouwers.forum_tools.fields import ForumToolsIDField
from brouwers.kits.fields import KitsManyToManyField


def get_build_slug(build):
    return u"{username} {title}".format(**{
        'username': build.user.username,
        'title': build.title
    })


class Build(models.Model):
    """
    Model for users to log their builds.
    """
    # owner
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # build information
    title = models.CharField(_("title"), max_length=255, help_text=_("Enter a descriptive build title."))
    slug = AutoSlugField(_('slug'), unique=True, populate_from=get_build_slug)

    # kit information
    kits = KitsManyToManyField(blank=True, verbose_name=_('kits'), related_name='builds')

    # topic information
    topic = ForumToolsIDField(_('build report topic'), type='topic', blank=True, null=True, unique=True)
    topic_start_page = models.PositiveSmallIntegerField(_('topic start page'), default=1)

    # build information
    start_date = models.DateField(_("start date"), blank=True, null=True)
    end_date = models.DateField(_("end date"), blank=True, null=True)

    class Meta:
        verbose_name = _("build report")
        verbose_name_plural = _("build reports")
        ordering = ['kits__scale', 'kits__brand__name']

    def __unicode__(self):
        return _(u"%(username)s - %(title)s") % {'username': self.user.username, 'title': self.title}

    def get_absolute_url(self):
        return reverse('builds:detail', kwargs={'slug': self.slug})

    @property
    def topic_url(self):
        """
        Build the PHPBB3 url based on topic (and forum) id.
        """
        if not self.topic:
            return None

        url = self.topic.get_absolute_url()
        if self.topic_start_page > 1:
            offset = settings.PHPBB_POSTS_PER_PAGE * (self.topic_start_page - 1)
            url += '&start={0}'.format(offset)
        return url

    @cached_property
    def brands(self):
        return set([kit.brand for kit in self.kits.all()])

    @cached_property
    def scales(self):
        return set([kit.scale for kit in self.kits.all()])


class BuildPhoto(models.Model):
    build = models.ForeignKey(Build, verbose_name=_(u'build'), related_name='photos', on_delete=models.CASCADE)
    photo = models.OneToOneField('albums.Photo', blank=True, null=True, on_delete=models.CASCADE)
    photo_url = models.URLField(blank=True, help_text=_('Link to an image'))
    order = models.PositiveSmallIntegerField(help_text=_('Order in which photos are shown'), blank=True, null=True)

    class Meta:
        verbose_name = _(u'build photo')
        verbose_name_plural = _(u'build photos')
        ordering = ['order', 'id']

    def __unicode__(self):
        return _(u"Photo for build %(build)s") % {'build': self.build.title}

    def clean(self):
        if not self.photo and not self.photo_url:
            raise ValidationError(_('Provide either an album photo or a link to a photo.'))

    @property
    def image(self):
        """
        Returns a cropping-suitable image.
        """
        if self.photo:
            return self.photo.image
        return self.photo_url
