import logging

from django.core.management.base import BaseCommand

from sorl.thumbnail import get_thumbnail

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    sizes = (
        "300x225",
        "1024",
        "1280x1280",
        "1024x1024",
    )

    def handle(self, *args, **options):
        from brouwers.albums.models import Photo

        for photo in Photo.objects.all():
            for size in self.sizes:
                try:
                    get_thumbnail(photo.image, size, upscale=False)
                except Exception as e:
                    logger.exception(e)
