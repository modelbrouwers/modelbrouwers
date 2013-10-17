from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _


from awards.models import Project, Category
from general.models import UserProfile
from kitreviews.models import Brand #TODO: FK to scale
from utils.slugify import unique_slugify


import urllib
import os


class Build(models.Model):
    """ Model to hold all information on a particular build of a user """
    # owner
    profile = models.ForeignKey(UserProfile)
    user = models.ForeignKey(User, null=True)

    # slug based on user-brand-scale-title
    slug = models.SlugField(_('slug'), unique=True)

    # topic information
    # allow external urls? Might be interesting!
    url = models.URLField(max_length=500, help_text=_("link to the build report"), unique=True)
    topic_id = models.PositiveIntegerField(
        _('Topic ID'), unique=True,
        blank=True, null=True,
        help_text=_('PHPBB topic id, used to build the link to the topic.')
        )
    forum_id = models.PositiveIntegerField(
        _('Forum ID'),
        blank=True, null=True,
        help_text=_('Used to determine the \'category\'.')
        )

    # kit information
    title = models.CharField(_("title"), max_length=255, 
        help_text=_("Enter a descriptive build title."))
    scale = models.PositiveSmallIntegerField(_("scale"), blank=True, null=True,
        help_text=_('Enter the number after the "1:" or "1/". E.g. 1/48 --> enter 48.'))
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name=_('brand'))
    
    # build information # TODO: jquery ui date
    start_date = models.DateField(_("start date"), blank=True, null=True)
    end_date = models.DateField(_("end date"), blank=True, null=True)
    

    # images TODO: replace with m2m album images
    img1 = models.URLField(_("Photo 1"), max_length=255, blank=True, help_text=_("Enter a link to a photo"))
    img2 = models.URLField(_("Photo 2"), max_length=255, blank=True, help_text=_("Enter a link to a photo"))
    img3 = models.URLField(_("Photo 3"), max_length=255, blank=True, help_text=_("Enter a link to a photo"))
    

    class Meta:
        verbose_name = _("build report")
        verbose_name_plural = _("build reports")
        ordering = ['profile', 'scale', 'brand__name']
    
    def __unicode__(self):
        return _("%(nickname)s - %(title)s") % {'nickname': self.profile.forum_nickname, 'title': self.title}
    
    # override save to generate slug
    def save(self, *args, **kwargs):
        if not self.slug:
            value = "%(username)s %(brand)s %(scale)s %(title)s" % {
                'username': self.user.username,
                'brand': self.brand.name or '',
                'scale': self.get_scale('-'),
                'title': self.title
            }

            unique_slugify(self, value)
        super(Build, self).save(*args, **kwargs)

    # URLS
    def get_absolute_url(self):
        return reverse('builds:detail', kwargs={'slug': self.slug}) 
    
    def get_topic_url(self):
        """ Build the PHPBB3 url based on topic (and forum) id. """
        query_params = SortedDict()
        query_params['t'] = self.topic_id
        if self.forum_id:
            query_params['f'] = self.forum_id
        
        query_string = urllib.urlencode(query_params)
        return os.path.join(settings.PHPBB_URL, 'viewtopic.php?%s' % query_string)

    @property
    def topic_url(self):
        """ 
        Return the url to the topic.

        Always give precedence to the url in database, as it can point to a
        specific post. If no url was supplied, try building the url from topic
        and forum id.
        """
        if self.url:
            return self.url
        return self.get_topic_url()

    def get_scale(self, separator=':'):
        if self.scale:
            return "1%s%s" % (separator, self.scale)
        return ''

    def get_brand_name(self):
        """ Deprecated """
        return self.brand.name


class BuildPhoto(models.Model):
    build = models.ForeignKey(Build, verbose_name = _(u'build'))
    photo = models.OneToOneField('albums.Photo', blank=True, null=True)
    photo_url = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = _(u'build photo')
        verbose_name_plural = _(u'build photos')
        ordering = ['order']

    def __unicode__(self):
        return _("Photo for build %(build)s") % {'build': self.build.title}

    def clean(self):
        if not self.photo and not self.photo_url:
            raise ValidationError(_('Provide either an album photo'
                                    ' or a link to a photo.'))

