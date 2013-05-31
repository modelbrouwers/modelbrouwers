from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
import zlib

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

class ForumUser(models.Model): # phpBB3 tables
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text=_("Primary key")
    )
    username = models.CharField(_("username"), max_length=255)
    user_posts = models.IntegerField()
    user_email = models.CharField(_("email"), max_length=100)
    user_email_hash = models.BigIntegerField(db_column="user_email_hash",
        # bigint(20)
        default=0,
        help_text=_("A hash of the user's email address.")
    )
    
    class Meta:
        verbose_name = _("forum user")
        verbose_name_plural = _("forum users")
        ordering = ('username',)
        managed = False
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
        super(ForumUser, self).save(*args, **kwargs)

class Report(models.Model):
    report_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="Primary key"
    )
    #reason_id = FK to reasons, not implement in Django yet
    report_closed = models.BooleanField(_('closed'), help_text=_('Closed reports need no more attention.'))
    report_time_int = models.IntegerField(_('time'), db_column="report_time", help_text=_('UNIX time when the report was added.'))
    report_text = models.TextField('text', blank=True)
    
    class Meta:
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


