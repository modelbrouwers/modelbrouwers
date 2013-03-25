from django.db import models
from django.utils.translation import ugettext_lazy as _

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
