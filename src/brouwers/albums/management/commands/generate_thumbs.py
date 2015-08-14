from django.core.management.base import NoArgsCommand

from sorl.thumbnail import get_thumbnail


class Command(NoArgsCommand):

    sizes = (
        '300x225',
        '1280',
        '1280x1280',
        '1024x1024',
    )

    def handle_noargs(self, *args, **options):
        from brouwers.albums.models import Photo

        for photo in Photo.objects.all():
            for size in self.sizes:
                get_thumbnail(photo.image, size)
