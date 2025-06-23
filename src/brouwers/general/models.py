from __future__ import annotations

from datetime import date
from typing import ClassVar

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import get_language, gettext_lazy as _

from brouwers.awards.models import Category

from .fields import CountryField


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # awardsinfo
    last_vote = models.DateField(default=date(2010, 1, 1))
    forum_nickname = models.CharField(max_length=30, unique=True)
    exclude_from_nomination = models.BooleanField(
        _("exclude me from nominations"),
        help_text=_("If checked, you will be excluded from Awards-nominations."),
        default=False,
    )
    categories_voted = models.ManyToManyField(Category, blank=True)

    # address
    street = models.CharField(_("street name"), max_length=255, blank=True, null=True)
    number = models.CharField(
        _("number"),
        max_length=10,
        help_text=_("house number (+ PO box if applicable)"),
        blank=True,
    )
    postal = models.CharField(_("postal code"), max_length=10, blank=True)
    city = models.CharField(_("city"), max_length=255, blank=True)
    province = models.CharField(_("province"), max_length=255, blank=True)
    country = CountryField(blank=True)

    class Meta:
        verbose_name = _("userprofile")
        verbose_name_plural = _("userprofiles")
        ordering = ["forum_nickname"]

    def __str__(self):
        return self.forum_nickname

    def full_name(self):
        return self.user.get_full_name()

    @property
    def is_address_ok(self):
        ok = False
        if self.street and self.number and self.postal and self.city and self.country:
            ok = True
        return ok


class RegistrationAttempt(models.Model):
    # same as forum_nickname
    username = models.CharField(
        _("username"), max_length=512, db_index=True, default="_not_filled_in_"
    )
    email = models.EmailField(_("email"), max_length=255, blank=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_("IP address"), db_index=True)
    success = models.BooleanField(_("success"), default=False)

    # keeping spam out
    potential_spammer = False
    type_of_visitor = models.CharField(
        _("type of visitor"), max_length=255, default="normal user"
    )
    ban = models.OneToOneField(
        "banning.Ban", blank=True, null=True, on_delete=models.SET_NULL
    )
    ban_id: int | None

    class Meta:
        verbose_name = _("registration attempt")
        verbose_name_plural = _("registration attempts")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.username

    @admin.display(description=_("is banned"), boolean=True)
    def is_banned(self) -> bool:
        return self.ban_id is not None


class AnnouncementManager(models.Manager["Announcement"]):
    def get_current(self) -> Announcement | None:
        qs = self.get_queryset()
        now = timezone.now()
        lang_code = get_language()[:2]
        q = Q(to_date__lt=now) | Q(from_date__gt=now)
        return qs.filter(language=lang_code).exclude(q).first()


class Announcement(models.Model):
    text = models.TextField()
    language = models.CharField(
        _("language"), max_length=10, choices=settings.LANGUAGES
    )
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)

    objects: ClassVar[  # pyright: ignore[reportIncompatibleVariableOverride]
        AnnouncementManager
    ] = AnnouncementManager()

    class Meta:
        verbose_name = _("announcement")
        verbose_name_plural = _("announcements")
        ordering = ["-from_date"]

    def __str__(self):
        return strip_tags(self.text[:50])
