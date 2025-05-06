import logging
from urllib.request import HTTPError

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField
from sorl.thumbnail.shortcuts import get_thumbnail

from brouwers.forum_tools.fields import ForumToolsIDField
from brouwers.kits.fields import KitsManyToManyField

from .validators import validate_image_url

logger = logging.getLogger(__name__)


def get_build_slug(build):
    return "{username} {title}".format(
        **{"username": build.user.username, "title": build.title}
    )


class Build(models.Model):
    """
    Model for users to log their builds.
    """

    # owner
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # build information
    title = models.CharField(
        _("title"), max_length=255, help_text=_("Enter a descriptive build title.")
    )
    slug = AutoSlugField(_("slug"), unique=True, populate_from=get_build_slug)

    # kit information
    kits = KitsManyToManyField(
        blank=True, verbose_name=_("kits"), related_name="builds"
    )

    # topic information
    topic = ForumToolsIDField(
        _("build report topic"), type="topic", blank=True, null=True, unique=True
    )
    topic_start_page = models.PositiveSmallIntegerField(
        _("topic start page"), default=1
    )

    # build information
    start_date = models.DateField(_("start date"), blank=True, null=True)
    end_date = models.DateField(_("end date"), blank=True, null=True)

    class Meta:
        verbose_name = _("build report")
        verbose_name_plural = _("build reports")
        ordering = ["kits__scale", "kits__brand__name"]

    def __str__(self):
        return _("%(username)s - %(title)s") % {
            "username": self.user.username,
            "title": self.title,
        }

    def get_absolute_url(self):
        return reverse("builds:detail", kwargs={"slug": self.slug})

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
            url += "&start={0}".format(offset)
        return url

    @cached_property
    def brands(self):
        return set([kit.brand for kit in self.kits.all()])

    @cached_property
    def scales(self):
        return set([kit.scale for kit in self.kits.all()])


class BuildPhoto(models.Model):
    build = models.ForeignKey(
        Build, verbose_name=_("build"), related_name="photos", on_delete=models.CASCADE
    )
    photo = models.OneToOneField(
        "albums.Photo", blank=True, null=True, on_delete=models.CASCADE
    )
    photo_url = models.URLField(
        blank=True,
        help_text=_("Link to an image"),
        validators=[validate_image_url],
    )
    order = models.PositiveSmallIntegerField(
        help_text=_("Order in which photos are shown"), blank=True, null=True
    )

    # photo_urls links break all the time and clog logs/error monitoring...
    image_gone = models.BooleanField(
        _("image gone"),
        default=False,
    )

    class Meta:
        verbose_name = _("build photo")
        verbose_name_plural = _("build photos")
        ordering = ["order", "id"]

    def __str__(self):
        return _("Photo for build %(build)s") % {"build": self.build.title}

    def clean(self):
        if not self.photo and not self.photo_url:
            raise ValidationError(
                _("Provide either an album photo or a link to a photo.")
            )

    def _get_image_thumbnail(self, geometry: str, options: dict) -> str:
        """
        Produce a thumbnail URL if possible, otherwise fall back to a fallback image.

        If the file uses a remote image URL which doesn't resolve (anymore), the image
        is marked as gone.
        """
        FALLBACK = static("images/thumb.400x300.png")

        # own albums -> files are not deleted
        if self.photo_id:
            return get_thumbnail(self.photo.image, geometry, **options).url

        if self.image_gone or not self.photo_url:
            return FALLBACK

        # try to obtain a thumbnail from the remote
        try:
            thumbnail = get_thumbnail(self.photo_url, geometry, **options)
            if thumbnail.exists():
                return thumbnail.url
        except HTTPError as exc:
            logger.warning(
                "Image at %s appears to be gone",
                self.photo_url,
                extra={"pk": self.pk},
                exc_info=exc,
            )

        # at this point, we couldn't write a thumbnail - mark the photo URL as broken
        # and fall back instead
        self.image_gone = True
        self.save()

        return FALLBACK

    @property
    def image_thumbnail(self) -> str:
        """
        Produce a thumbnail URL if possible, otherwise fall back to a fallback image.

        If the file uses a remote image URL which doesn't resolve (anymore), the image
        is marked as gone.
        """
        return self._get_image_thumbnail("400x300", {"padding": True})

    @property
    def preview_image(self) -> str:
        return self._get_image_thumbnail("1024", {})
