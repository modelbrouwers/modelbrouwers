from django.db import models


class AlbumManager(models.Manager):

    def for_index(self):
        qs = self.public().select_related('user', 'cover')
        return qs.order_by('-last_upload')

    def public(self):
        return self.get_queryset().filter(trash=False, public=True)


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
