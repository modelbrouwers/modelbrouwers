import urllib

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from brouwers.albums.models import Album


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
        params = {'hash': self.hash, 'forum_nickname': self.username}
        query_string = urllib.urlencode(dict([k, v] for k, v in params.items()))
        return u"http://modelbrouwers.nl/confirm_account/?%s" % (query_string)


class AlbumUserMigration(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    django_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    class Meta:
        verbose_name = _("album user migration")
        verbose_name_plural = _("album user migrations")

    def __unicode__(self):
        if self.django_user:
            django_user = self.django_user.__unicode__() + " (%s)" % self.django_user.email
        else:
            django_user = "[django user not found]"
        return u"%s (%s) -> %s" % (self.username, self.email, django_user)


class AlbumMigration(models.Model):
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024, blank=True)
    owner = models.ForeignKey(AlbumUserMigration)
    migrated = models.NullBooleanField(blank=True, null=True)
    new_album = models.ForeignKey(Album, blank=True, null=True)

    class Meta:
        ordering = ('owner', 'title')

    def __unicode__(self):
        return u"%s" % self.title


class PhotoMigration(models.Model):
    album = models.ForeignKey(AlbumMigration)
    filepath = models.CharField(max_length=80)
    filename = models.CharField(max_length=256)
    pwidth = models.PositiveIntegerField(blank=True, null=True)
    pheight = models.PositiveIntegerField(blank=True, null=True)
    owner = models.ForeignKey(AlbumUserMigration)
    title = models.CharField(max_length=512, blank=True)
    caption = models.CharField(max_length=1024, blank=True)
    migrated = models.NullBooleanField()

    class Meta:
        ordering = ('album',)

    def __unicode__(self):
        return u"%(path)s%(filename)s" % {'path': self.filepath, 'filename': self.filename}
