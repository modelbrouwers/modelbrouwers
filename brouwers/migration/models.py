from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class UserMigration(models.Model):
    username = models.CharField(max_length=50) #actually 20
    username_clean = models.CharField(max_length=50) #lowercase version
    email = models.EmailField(max_length=254)
    hash = models.CharField(max_length=256, blank=True, null=True)
    
    class Meta:
        ordering = ['username_clean']
    
    def __unicode__(self):
        return u"%s" % self.username
    
    def save(self, *args, **kwargs):
        if not self.username_clean:
            self.username_clean = self.username.lower()
        super(UserMigration, self).save(*args, **kwargs)
    
    @property
    def url(self):
        return u"http://modelbrouwers.nl/confirm_account/?hash=%s&forum_nickname=%s" % (self.hash, self.username)

class AlbumUserMigration(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    django_user = models.ForeignKey(User, blank=True, null=True)
    
    class Meta:
        verbose_name = _("album user migration")
        verbose_name_plural = _("album user migrations")
    
    def __unicode__(self):
        if self.django_user:
            django_user = self.django_user.__unicode__() + " (%s)" % self.django_user.email
        else:
            django_user = "[django user not found]"
        return u"%s (%s) -> %s" % (self.username, self.email, django_user)
