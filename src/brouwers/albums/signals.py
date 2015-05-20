from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Photo


@receiver(post_save, sender=Photo, dispatch_uid='album.set_last_upload')
def set_last_upload(sender, instance, created, raw, **kwargs):
    if raw:
        return

    if created:
        instance.album.last_upload = instance.uploaded
        instance.album.save()
