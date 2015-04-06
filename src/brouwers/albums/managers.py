from django.db import models


class AlbumsManager(models.Manager):

    def for_index(self):
        qs = self.public().select_related('user', 'cover')
        return qs.order_by('-last_upload')

    def public(self):
        return self.get_queryset().filter(trash=False, public=True)
