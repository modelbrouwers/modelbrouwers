from zipfile import ZipFile

from django.core.management import BaseCommand
from django.db import transaction
from django.forms.models import model_to_dict
from django.utils import timezone

from ...models import DataDownloadRequest


class DataDownload(object):
    def __init__(self, download_request):
        self.download_request = download_request
        self.zip = ZipFile('/tmp/out', 'w')

    @transaction.atomic
    def process(self):
        self.prepare()
        transaction.on_commit(self.email)
        self.download_request.finished = timezone.now()
        self.download_request.save()

    def prepare(self):
        """
        Gather all the data related to the user.
        """
        user = self.download_request.user

        # albums
        albums = user.album_set.all()
        album_groups = user.albumgroup_set.all()
        photos = user.photo_set.all()  # todo: link to the album page
        downloads = user.albumdownload_set.all()

        # awards
        submitted_projects = user.nominations.all()
        nomination_votes = user.vote_set.all()

        # banning
        bans = user.ban_set.all()

        # brouwersdag
        showcased_models = user.showcasedmodel_set.all()

        # builds
        builds = user.build_set.prefetch_related('photos')

        # kitreviews
        reviews = user.kitreview_set.all()  # TODO: KR properties and property ratings
        review_votes = user.kitreviewvote_set.all()

        # online_users
        tracked_users = user.trackeduser

        # users
        data_downloads = user.datadownloadrequest_set.all()

        # TODO: forum posts
        # TODO: shop?


        import bpdb; bpdb.set_trace()

    def email(self):
        import bpdb; bpdb.set_trace()


class Command(BaseCommand):
    help = "Process the pending data download requests"

    def handle(self, **options):
        open_requests = (
            DataDownloadRequest.objects
            .select_related('user')
            .filter(finished__isnull=True)
        )
        for download_request in open_requests:
            download = DataDownload(download_request)
            download.process()
