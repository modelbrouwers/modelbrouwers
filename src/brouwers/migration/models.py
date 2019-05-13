from django.conf import settings
from django.db import models
from django.utils.http import urlencode
from django.utils.translation import ugettext as _

from brouwers.albums.models import Album


class UserMigration(models.Model):
    username = models.CharField(max_length=50)  # actually 20
    username_clean = models.CharField(max_length=50)  # lowercase version
    email = models.EmailField(max_length=254)
    hash = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ['username_clean']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username_clean:
            self.username_clean = self.username.lower()
        super(UserMigration, self).save(*args, **kwargs)

    @property
    def url(self):
        params = {'hash': self.hash, 'forum_nickname': self.username}
        query_string = urlencode(dict([k, v] for k, v in params.items()))
        return "http://modelbrouwers.nl/confirm_account/?%s" % (query_string)


class AlbumUserMigration(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    django_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("album user migration")
        verbose_name_plural = _("album user migrations")

    def __str__(self):
        if self.django_user:
            django_user = "%s (%s)" % (self.django_user, self.django_user.email)
        else:
            django_user = "[django user not found]"
        return "%s (%s) -> %s" % (self.username, self.email, django_user)


class AlbumMigration(models.Model):
    title = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024, blank=True)
    owner = models.ForeignKey(AlbumUserMigration, on_delete=models.CASCADE)
    migrated = models.NullBooleanField(blank=True, null=True)
    new_album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('owner', 'title')

    def __str__(self):
        return self.title


class PhotoMigration(models.Model):
    album = models.ForeignKey(AlbumMigration, on_delete=models.CASCADE)
    filepath = models.CharField(max_length=80)
    filename = models.CharField(max_length=256)
    pwidth = models.PositiveIntegerField(blank=True, null=True)
    pheight = models.PositiveIntegerField(blank=True, null=True)
    owner = models.ForeignKey(AlbumUserMigration, on_delete=models.CASCADE)
    title = models.CharField(max_length=512, blank=True)
    caption = models.CharField(max_length=1024, blank=True)
    migrated = models.NullBooleanField()

    class Meta:
        ordering = ('album',)

    def __str__(self):
        return "%(path)s%(filename)s" % {'path': self.filepath, 'filename': self.filename}
