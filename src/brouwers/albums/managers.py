from django.core.cache import cache
from django.db import models


class AlbumQueryset(models.QuerySet):

    def active(self):
        return self.filter(trash=False)

    def public(self):
        return self.filter(public=True).active()

    def for_index(self):
        qs = self.public().select_related('user', 'cover')
        return qs.order_by('-last_upload')

    def for_user(self, user):
        """
        Retrieve all albums that :param:`user` can read.
        """
        assert user.is_authenticated(), 'Anonymous user passed in'
        qs = self.filter(user=user)  # private and public
        qs2 = self.filter(albumgroup__users=user)
        return (qs | qs2).active().distinct()


def toggle_ordering(field):
    if field.startswith('-'):
        return field[1:]
    else:
        return u'-%s' % field


class PhotoManager(models.Manager):

    def next(self, current, user=None):
        # if user.is_authenticated():
        ordering = self.model._meta.ordering
        queryset = self.get_queryset().filter(
            album=current.album,
            order__gte=current.order
        ).exclude(pk=current.pk).order_by(*ordering)
        return queryset.first()

    def previous(self, current, user=None):
        # if user.is_authenticated():
        ordering = [toggle_ordering(field) for field in self.model._meta.ordering]
        queryset = self.get_queryset().filter(
            album=current.album,
            order__lte=current.order
        ).exclude(pk=current.pk).order_by(*ordering)
        return queryset.first()


class PreferencesManager(models.Manager):

    def get_for(self, user):
        """
        Get the preferences from the cache or fall back to the database.

        Anonymous users get the default values, while for logged in users the
        actual object is retrieved.
        """
        from .serializers import PreferencesSerializer

        if not user.is_authenticated():
            return PreferencesSerializer(self.model()).data

        key = self.model._get_cache_key(user.id)
        prefs = cache.get(key)
        if prefs is None:
            prefs_obj, created = self.get_or_create(user=user)
            prefs = prefs_obj.cache()
        return prefs
