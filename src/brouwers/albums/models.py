import os
import warnings
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from djchoices import DjangoChoices, ChoiceItem

from brouwers.forum_tools.fields import ForumToolsIDField
from .utils import rotate_img
from .managers import AlbumManager, PhotoManager, PreferencesManager


class Category(models.Model):
    name = models.CharField(_("name"), max_length=256, unique=True)
    order = models.PositiveSmallIntegerField(_("order"), default=1, blank=True, null=True)

    url = models.URLField(_("url"), max_length=500, blank=True)
    on_frontpage = models.BooleanField(_("on frontpage"), default=False)
    public = models.BooleanField(_("public"), default=True,
                                 help_text=_("If the category is public, regular"
                                             " users can add their albums to the"
                                             " category. If it isn't, only people"
                                             " with admin permissions can do so."))

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ['order', 'name']

    def __unicode__(self):
        return self.name


class Album(models.Model):

    class WritePermissions(DjangoChoices):
        owner = ChoiceItem('u', pgettext_lazy("write permissions for owner", "owner"))
        group = ChoiceItem('g', _('group'))
        everyone = ChoiceItem('o', _('everyone'))  # auth required

    # owner of the album
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, verbose_name=_("user"))
    title = models.CharField(_("album title"), max_length="256", db_index=True)
    clean_title = models.CharField(_("album title"), max_length="256", default='', blank=True)
    description = models.CharField(_("album description"), max_length=500, blank=True)
    category = models.ForeignKey(
        Category, blank=True, null=True,
        default=1, verbose_name=_("category"),
    )
    cover = models.ForeignKey(
        'Photo',
        blank=True,
        null=True,
        help_text=_("Image to use as album cover."),
        related_name='cover',
        verbose_name=_("cover")
    )

    # Logging and statistics
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(_("last modified"), auto_now=True)
    last_upload = models.DateTimeField(
        default=datetime(1970, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc),
        db_index=True
    )
    views = models.PositiveIntegerField(default=0)

    # User preferences
    order = models.PositiveSmallIntegerField(_("order"), default=1, blank=True, null=True, db_index=True)
    public = models.BooleanField(
            _("Public?"),
            help_text=_("Can this album be viewed by everyone? Untick to make the album available only to yourself."),
            default=True
        )

    # Misc features
    topic = ForumToolsIDField(_('build report topic'), blank=True, null=True, type='topic')
    # albums can be voted, so we can have an 'album of the month' feature
    votes = models.IntegerField(_("appreciation"), default=0)
    # writable to only user, group or everyone (unix like permissions)
    writable_to = models.CharField(
        _("writable to"), max_length=1,
        choices=WritePermissions.choices, default=WritePermissions.owner,
        help_text=_('Specify who can upload images in this album')
    )
    trash = models.BooleanField(default=False)  # put in trash before removing from db

    objects = AlbumManager()

    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")
        # order_with_respect_to = "user"
        ordering = ('order', 'title')
        unique_together = (('user', 'title'),)
        permissions = (
            ('edit_album', _("Can edit/remove album")),
            ('see_all_albums', _("Can see all albums")),
            ('access_albums', _("Can use new albums")),
        )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.trash and self.clean_title != self.title:
            self.clean_title = self.title
        super(Album, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('albums:detail', args=[self.id])

    def get_cover(self):
        if self.cover:
            return self.cover

        img = self.photo_set.filter(trash=False).order_by('order').first()
        if img is not None:
            self.cover = img  # save the cover to perform optimalization if no cover is set
            self.save()
        return img

    def set_order(self):
        max_order = Album.objects.filter(user=self.user, trash=False).aggregate(Max('order'))['order__max'] or 0
        self.order = max_order+1
        return self


class AlbumGroup(models.Model):
    album = models.OneToOneField(
            Album, verbose_name=_("album"),
            help_text=_("Album for which the group has write permissions."),
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("users"),
        help_text=_("Users who can write in this album."),
        blank=True
    )

    class Meta:
        verbose_name = _("album group")
        verbose_name_plural = _("album groups")
        ordering = ('album',)

    def __unicode__(self):
        return _(u"Write permissions for '%(album)s'") % {'album': self.album.__unicode__()}


def get_image_path(instance, filename):
    name, extension = os.path.splitext(filename)
    filename = name + extension
    return os.path.join('albums', str(instance.album.user.id), str(instance.album.id), filename)


class Photo(models.Model):
    """ Model Fields """
    # image properties
    user = models.ForeignKey(settings.AUTH_USER_MODEL)  # we need to know the owner (public albums)
    album = models.ForeignKey(Album, db_index=True)
    width = models.PositiveSmallIntegerField(_("width"), blank=True, null=True)
    height = models.PositiveSmallIntegerField(_("height"), blank=True, null=True)
    image = models.ImageField(
        _("image"), max_length=200, upload_to=get_image_path,
        height_field='height', width_field='width'
    )
    description = models.CharField(_("photo description"), max_length=500, blank=True)

    # Logging and statistics
    uploaded = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(_("last modified"), auto_now=True)
    views = models.PositiveIntegerField(default=0)

    order = models.PositiveSmallIntegerField(default=1, blank=True, null=True, db_index=True)
    trash = models.BooleanField(default=False)

    objects = PhotoManager()

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")
        ordering = ['album', 'order', 'pk']

    def save(self, *args, **kwargs):
        if not self.pk:
            max_order = Photo.objects.filter(album=self.album).aggregate(max_order=Max('order'))['max_order'] or 0
            self.order = max_order + 1
        super(Photo, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'albumphoto %d' % self.id

    def get_absolute_url(self):
        return reverse('albums:photo-detail', kwargs={'pk': self.pk})

    @property
    def exists(self):
        """
        If a network storage is used, this can cause latency/slow pages.
        """
        return self.image.storage.exists(self.image.name)

    # TRANSFORMING OF IMAGE #################################
    def rotate_left(self):
        """ Rotate 90 degrees counter clock wise """
        rotate_img(self.image, degrees=90)
        self.save()

    def rotate_right(self):
        """ Rotate 90 degrees clock wise """
        rotate_img(self.image, degrees=-90)
        self.save()


class Backgrounds(DjangoChoices):
    black = ChoiceItem('black', _('Black'))
    white = ChoiceItem('white', _('White'))
    grey = ChoiceItem('EEE', _('Light grey'))
    dark_grey = ChoiceItem('333', _('Dark grey'))


def validate_backgrounds(value):
    return Backgrounds.validator(value)


class Preferences(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    # options for uploadify
    auto_start_uploading = models.BooleanField(
        _("start uploading automatically?"),
        help_text=_("Start upload automatically when files are selected"),
        default=False)

    # sidebar settings
    collapse_sidebar = models.BooleanField(
        _("collapse sidebar"), default=True,
        help_text=_("Show the sidebar as closed when typing a post.")
        )
    hide_sidebar = models.BooleanField(
        _("hide sidebar"), default=False,
        help_text=_("Hide the sidebar completely when typing a post and activate it with a button.")
        )
    sidebar_bg_color = models.CharField(
        _("sidebar background color"),
        max_length=7, help_text=_("Background for the overlay in the board."),
        choices=Backgrounds.choices, default=Backgrounds.black,
        validators=[validate_backgrounds]
    )
    sidebar_transparent = models.BooleanField(_("transparent background?"), default=True)
    text_color = models.CharField(
        _("sidebar text color"), max_length=7, blank=True,
        help_text=_("Text color in the overlay. HTML color format #xxxxxx or #xxx.")
    )
    width = models.CharField(
        _("sidebar width"), max_length=6, blank=True,
        help_text=_("Width of the sidebar. E.g. '30%' or '300px'.")
    )

    objects = PreferencesManager()

    class Meta:
        verbose_name = _("User preferences")
        verbose_name_plural = verbose_name
        ordering = ('user',)

    def __unicode__(self):
        user = self.user.get_full_name() if self.id else 'Anonymous user'
        return _(u"Preferences for %(user)s") % {'user': user}

    @classmethod
    def get_or_create(cls, user):
        warnings.warn('Preferences.get_or_create is deprecated. Use Preferences'
                      '.objects.get_for(user)', DeprecationWarning)
        return cls.objects.get_for(user)

    @classmethod
    def _get_cache_key(cls, user_id):
        return 'album-preferences:%d' % user_id

    def cache(self):
        """
        Sets the serialized data in the cache.
        """
        from .serializers import PreferencesSerializer
        key = self._get_cache_key(self.user_id)
        serialized = PreferencesSerializer(self).data
        cache.set(key, serialized, 24*60*60)  # cache 24h
        return serialized


class AlbumDownload(models.Model):
    album = models.ForeignKey(Album)
    downloader = models.ForeignKey(settings.AUTH_USER_MODEL, help_text=_("user who downloaded the album"))
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    failed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("album download")
        verbose_name_plural = _("album downloads")
        ordering = ('-timestamp',)

    def __unicode__(self):
        return u"%s" % _("Download of %(album)s by %(username)s" % {
                'album': self.album.title,
                'username': self.downloader.username
                }
            )

from . import signals
