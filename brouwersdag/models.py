from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ShowCasedModel(models.Model):
    """ Model to track showcased scale models by users. """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('brouwer'), blank=True, null=True)
    owner_name = models.CharField(_('real name'), max_length=254)
    email = models.EmailField(_('e-mail address'))

    name = models.CharField(_('model name'), max_length=254)
    brand = models.ForeignKey('kitreviews.Brand', verbose_name=_('brand'), blank=True, null=True)
    scale = models.PositiveSmallIntegerField(_("scale"),
        help_text=_('Enter the number after the "1:" or "1/". E.g. 1/48 --> enter 48.'))
    remarks = models.TextField(_('remarkable elements'), blank=True,
        help_text=_('Add the features that make this model special here, e.g. "scratch built cockpit"'))

    topic = models.URLField(_('topic url'), blank=True)

    # dimensions
    length = models.PositiveSmallIntegerField(_('length'), null=True, blank=True, help_text=_('In cm.'))
    width = models.PositiveSmallIntegerField(_('width'), null=True, blank=True, help_text=_('In cm.'))
    height = models.PositiveSmallIntegerField(_('height'), null=True, blank=True, help_text=_('In cm.'))

    # competition?
    competition = models.ForeignKey('brouwersdag.Competition',
        null=True, blank=True, verbose_name=_('competition'))
    is_competitor = models.BooleanField(_('enter competition?'), default=False)
    is_paid = models.BooleanField(_('competition fee paid?'), default=False)

    # logging/status
    created = models.DateTimeField(_('added'), auto_now_add=True)

    class Meta:
        verbose_name = _(u'showcased model')
        verbose_name_plural = _(u'showcased models')

    def __unicode__(self):
        return self.name

    def get_scale(self):
        return "1:{0}".format(self.scale) if self.scale else ''

    def get_absolute_url(self):
        return reverse('brouwersdag:model-detail', kwargs={'pk': self.pk})

    def get_url(self):
        domain = Site.objects.get_current().domain
        return u'http://{0}{1}'.format(domain, self.get_absolute_url())


class Competition(models.Model):
    name = models.CharField(_('name'), max_length=100)
    price = models.DecimalField(_('price per model'), max_digits=5, decimal_places=2, default='0.0')

    max_num_models = models.PositiveSmallIntegerField(_('models per participant'),
        default=0, help_text=_('Maximum number of models per participant, enter 0 for unlimited.'))
    max_participants = models.PositiveSmallIntegerField(_('maximum number of participants'),
        default=0, help_text=_('Maximum number of participants, enter 0 for unlimited.'))

    is_current = models.BooleanField(_('current open competition?'),
        default=False, help_text=_('Marking this competition as active will deactivate all other competitions.'))

    class Meta:
        verbose_name = _(u'competition')
        verbose_name_plural = _(u'competitions')

    def save(self, *args, **kwargs):
        if self.is_current:
            Competition.objects.update(is_current=False)
        super(Competition, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def models(self):
        return self.showcasedmodel_set.filter(is_competitor=True)


class Brouwersdag(models.Model):
    name = models.CharField(_('name'), max_length=100)
    date = models.DateField(_('date'), null=True, blank=True)

    # TODO: open from (visitors, exhibitors), closing, special events
    class Meta:
        verbose_name = _(u'brouwersdag')
        verbose_name_plural = _(u'brouwersdagen')
        ordering = ('-date',)

    def __unicode__(self):
        return self.name or 'Brouwersdag %s' % self.date.year


class Exhibitor(models.Model):
    name = models.CharField(_('name'), max_length=100)
    website = models.URLField(_('website'), blank=True)

    brouwersdag = models.ForeignKey(Brouwersdag, blank=True, null=True)
    space = models.CharField(_('space needed'),  blank=True,
        max_length=100, help_text=_('Amount of space needed. 100 characters or less.'))

    class Meta:
        verbose_name = _(u'exhibitor')
        verbose_name_plural = _(u'exhibitors')
        ordering = ('name',)
        order_with_respect_to = 'brouwersdag'

    def __unicode__(self):
        return self.name
