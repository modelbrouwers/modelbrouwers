from django.db.models.signals import post_save
from django.dispatch import receiver

from sorl.thumbnail import get_thumbnail

from .models import Photo, Preferences


@receiver(post_save, sender=Photo, dispatch_uid='album.set_last_upload')
def set_last_upload(sender, instance, created, raw, **kwargs):
    if raw:  # pragma: no cover
        return

    if created:
        instance.album.last_upload = instance.uploaded
        instance.album.save()


@receiver(post_save, sender=Preferences, dispatch_uid='preferences.set_cache')
def update_cache(sender, instance, created, raw, **kwargs):
    if raw:  # pragma: no cover
        return
    instance.cache()


@receiver(post_save, sender=Photo, dispatch_uid='photo.generate_thumbs')
def generate_photo_thumbs(sender, instance, created, raw, **kwargs):
    if not created or raw:
        return

    sizes = (
        '300x225',
        '1280',
        '1280x1280',
        '1024x1024',
    )

    for size in sizes:
        get_thumbnail(instance.image, size, upscale=False)
