from django.db import models


class AlbumsManager(models.Manager):

    def for_index(self):
        qs = self.get_queryset().select_related('user', 'cover')
        return qs.filter(trash=False, public=True).order_by('-last_upload')
