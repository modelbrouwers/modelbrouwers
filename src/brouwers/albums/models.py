import os
from datetime import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

from djchoices import DjangoChoices, ChoiceItem

from brouwers.forum_tools.fields import ForumToolsIDField
from brouwers.general.utils import get_username as _get_username
from .utils import rotate_img
from .managers import AlbumsManager


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


def get_title():
    return "album %s" % timezone.now().strftime("%d-%m-%Y")


class Album(models.Model):

    class WritePermissions(DjangoChoices):
        owner = ChoiceItem('u', pgettext_lazy("write permissions for owner", "owner"))
        group = ChoiceItem('g', _('group'))
        everyone = ChoiceItem('o', _('everyone'))  # auth required

    # owner of the album
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True, verbose_name=_("user"))
    title = models.CharField(
        _("album title"), max_length="256", default=get_title, db_index=True
    )
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

    objects = AlbumsManager()

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
        return u"%s" % self.title

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

    def get_username(self):
        return _get_username(self)

    # TODO: fix in templates with get_cover_data, now deprecated
    @property
    def cover_thumb_url(self):
        img = self.get_cover()
        if img:
            return img.thumb_url
        return None

    # TODO: replace with sorl/easythumbnails
    def get_cover_data(self):
        cover = self.get_cover()
        data = {'cover': cover}
        if cover:
            data['width'] = cover.get_thumb_width()
            data['height'] = cover.get_thumb_height()
            data['width_200'] = cover.get_thumb_width_200()
            data['height_150'] = cover.get_thumb_height_150()
            data['width_100'] = cover.get_thumb_width_100()
            data['height_75'] = cover.get_thumb_height_75()
            data['thumb_url'] = cover.thumb_url
        return data

    def number_of_photos(self):
        return self.photo_set.filter(trash=False).count()

    def set_order(self):
        max_order = Album.objects.filter(user=self.user, trash=False).aggregate(Max('order'))['order__max'] or 0
        self.order = max_order+1
        return self


class AlbumGroup(models.Model):
    album = models.ForeignKey(
            Album,
            verbose_name=_("album"),
            help_text=_("Album for which the group has write permissions."),
            unique=True
            )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("users"),
        help_text=_("Users who can write in this album."),
        blank=True, null=True
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=True)  # we need to know the owner (public albums)
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

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")
        ordering = ['album', 'order', 'pk']

    def save(self, *args, **kwargs):
        # also save the album, so the last modified date gets set
        new = False
        if not self.id:
            new = True
        super(Photo, self).save(*args, **kwargs)
        if new:
            self.album.last_upload = self.uploaded
            self.album.save()

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

    def get_username(self):
        return _get_username(self)

    # TRANSFORMING OF IMAGE #################################
    def rotate_left(self):
        """ Rotate 90 degrees counter clock wise """
        rotate_img(self.image, degrees=90)
        self.save()

    def rotate_right(self):
        """ Rotate 90 degrees clock wise """
        rotate_img(self.image, degrees=-90)
        self.save()

    def get_next_previous(self, cmp='gt', order=['order', 'id']):
        filter_order = {'order__{0}'.format(cmp): self.order}
        filter_pk = {'pk__{0}'.format(cmp): self.pk}

        # see if there are photos with a different order
        base = Photo.objects.filter(album=self.album, trash=False).exclude(id=self.id)
        photos = base.filter(**filter_order).order_by(*order)[:1]
        if photos:
            return photos[0]

        photos = base.filter(order=self.order, **filter_pk).order_by(*order)[:1]
        if photos:
            return photos[0]
        return None

    def get_next(self):
        return self.get_next_previous(cmp='gt', order=['order', 'id'])

    def get_previous(self):
        return self.get_next_previous(cmp='lt', order=['-order', '-id'])

    def get_next_previous_batch(self, batch_size, cmp='gt'):
        assert cmp in ['gte', 'lte']
        filters = {
            'album': self.album,
            'order__{0}'.format(cmp): self.order,
            'trash': False
        }
        ordering = ['order', 'id'] if cmp == 'gte' else ['-order', '-id']
        return Photo.objects.filter(**filters).exclude(id=self.id).order_by(*ordering)[:batch_size] or []

    def get_next_3(self):
        return self.get_next_previous_batch(3, cmp='gte')

    def get_previous_3(self):
        return self.get_next_previous_batch(3, cmp='lte')

    def url_back_3(self):
        photos = self.get_next_previous_batch(4, cmp='lte')
        if len(photos) == 4:
            return photos[3].get_absolute_url()
        return None

    def url_forward_3(self):
        photos = self.get_next_previous_batch(4, cmp='gte')
        if len(photos) == 4:
            return photos[3].get_absolute_url()
        return None

    @property
    def BBCode(self):
        domain = Site.objects.get_current().domain
        return u'[IMG]http://%s%s[/IMG]' % (domain, self.image.url)

    @property
    def direct_link(self):
        domain = Site.objects.get_current().domain
        return u'http://%s%s' % (domain, self.image.url)

    @property
    def BBCode_1024(self):
        domain = Site.objects.get_current().domain
        path, f = os.path.split(self.image.url)
        return u'[IMG]http://%s%s/1024_%s[/IMG]' % (domain, path, f)

    @property
    def thumb_url(self):
        # TODO: replace with sorl/easy thumbnail
        path, f = os.path.split(self.image.url)
        thumb_prefix = settings.THUMB_DIMENSIONS[2]
        if self.width < settings.THUMB_DIMENSIONS[0] or self.height < settings.THUMB_DIMENSIONS[1]:
            thumb_prefix = ''
        return u"%s/%s%s" % (path, thumb_prefix, f)

    @property
    def is_wider_than_higher(self):
        ratio = float(self.width) / float(self.height)
        if ratio >= 1.333:
            return True
        return False

    def get_thumb_height(self, width=140, height=105):
        if self.is_wider_than_higher:
            ratio = float(self.width) / float(self.height)
            height = int(width/ratio)
        if self.height < height:
            height = self.height
        return height

    def get_thumb_width(self, width=140, height=105):
        if self.width and self.width < width:
            width = self.width
        elif not self.is_wider_than_higher:
            ratio = float(self.width) / float(self.height)
            width = int(ratio*height)
        return width

    def get_thumb_width_200(self):
        return self.get_thumb_width(width=200, height=150)

    def get_thumb_height_150(self):
        return self.get_thumb_height(width=200, height=150)

    def get_thumb_width_100(self):
        return self.get_thumb_width(width=100, height=75)

    def get_thumb_height_75(self):
        return self.get_thumb_height(width=100, height=75)

IMG_SIZES = (
    (0, "1024x768"),
    (1, "800x600"),
    (2, "1024x1024"),
    (3, "800x800"),
)
UPLOADER_CHOICES = (
    ("F", _("Multiple files at once")),
    ("H", _("Basic")),
)
BACKGROUND_CHOICES = (
    ("black", _("Black")),
    ("white", _("White")),
    ("EEE", _("Light grey")),
    ("333", _("Dark grey")),
)


# only create this object when user visits preferences page first time, otherwise go with the defaults
class Preferences(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    default_img_size = models.PositiveSmallIntegerField(
        _("default image dimensions"),
        choices=IMG_SIZES,
        default=0,
        help_text=_("Your pictures will be scaled to this size.")
    )
    default_uploader = models.CharField(
        _("default uploader"),
        max_length=1,
        choices=UPLOADER_CHOICES, default="F",
        help_text=_("""Multiple files at once makes use of a Flash uploader,
you select all your files without having to click too much buttons.
The basic uploader has a file field for each image.""")
    )
    # options for uploadify
    auto_start_uploading = models.BooleanField(
        _("start uploading automatically?"),
        help_text=_("Start upload automatically when files are selected"),
        default=False)
    show_direct_link = models.BooleanField(_("Show direct links under the photo"), default=False)

    # admin options
    apply_admin_permissions = models.BooleanField(
        help_text=_("When checked, you will see all the albums and be able to edit them."),
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
        max_length=7, blank=True,
        help_text=_("Background for the overlay in the board."),
        choices=BACKGROUND_CHOICES, default='black'
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

    class Meta:
        verbose_name = _("User preferences")
        verbose_name_plural = verbose_name
        ordering = ('user',)

    def save(self, *args, **kwargs):
        from .serializers import PreferencesSerializer
        super(Preferences, self).save(*args, **kwargs)
        # update the cache
        if kwargs.get('commit', True):
            key = self.get_cache_key()
            cache.set(key, PreferencesSerializer(self).data)

    def __unicode__(self):
        if self.id:
            user = self.user.get_full_name()
        else:
            user = 'Anonymous user'
        return _(u"Preferences for %(user)s") % {'user': user}

    @classmethod
    def get_or_create(cls, user):
        """ Get the preferences from the cache or fall back to the database """
        # TODO: move to manager
        from .serializers import PreferencesSerializer

        # anonymous users get the defaults
        if not user.is_authenticated():
            prefs_obj = Preferences()
            return PreferencesSerializer(prefs_obj).data

        key = 'album-preferences:%d' % user.id
        prefs = cache.get(key)
        if prefs is None:
            prefs_obj, created = Preferences.objects.get_or_create(user=user)
            prefs = PreferencesSerializer(prefs_obj).data
            cache.set(key, prefs, 24*60*60)  # cache a whole day
        return prefs

    def get_cache_key(self, user_id=None):
        """ FIXME: remove DRY violation """
        user_id = user_id or self.user_id
        return 'album-preferences:%d' % user_id


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
