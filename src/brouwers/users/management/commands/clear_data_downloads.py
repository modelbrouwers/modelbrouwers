from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from ...models import DataDownloadRequest


class Command(BaseCommand):
    help = "Clear the downloaded requests to free up disk space"

    def handle(self, **options):
        hour_ago = timezone.now() - timedelta(hours=1)
        downloaded_requests = (
            DataDownloadRequest.objects
            .filter(downloaded__lt=hour_ago)
            .exclude(zip_file='')
        )
        self.stdout.write("Clearing {count} files".format(count=downloaded_requests.count()))
        for download_request in downloaded_requests:
            download_request.zip_file.delete(save=True)
