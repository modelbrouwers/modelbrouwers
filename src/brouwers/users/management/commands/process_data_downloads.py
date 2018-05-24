import os
import shutil
import tempfile
from zipfile import ZipFile

from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Prefetch
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.utils import timezone

from brouwers.builds.models import BuildPhoto

from ...models import DataDownloadRequest


class DataDownload(object):
    def __init__(self, download_request):
        self.download_request = download_request
        self.tempdir = tempfile.mkdtemp()

        print(self.tempdir)

        # self.zip = ZipFile('/tmp/out', 'w')

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
        nomination_votes = (
            user.vote_set
            .select_related('category', 'project1', 'project2', 'project3')
        )

        # banning
        bans = user.ban_set.all()

        # brouwersdag
        showcased_models = user.showcasedmodel_set.all()

        # builds
        builds = user.build_set.prefetch_related(
            Prefetch('photos', queryset=BuildPhoto.objects.filter(photo__isnull=False)),
            'kits'
        )

        # kitreviews
        reviews = user.kitreview_set.all()
        # TODO: KR properties and property ratings
        # review_votes = user.kitreviewvote_set.all()

        # online_users
        tracked_user = user.trackeduser if hasattr(user, 'trackeduser') else None

        # users
        data_downloads = user.datadownloadrequest_set.all()

        # TODO: forum posts
        # TODO: shop?
        templates_and_data = (
            ('data-download/index.html', {'request': self.download_request}),
            ('data-download/profile.html', {'user': user}),
            ('data-download/albums.html', {'albums': albums}),
            ('data-download/album_groups.html', {'album_groups': album_groups}),
            ('data-download/photos.html', {'photos': photos}),
            ('data-download/album_downloads.html', {'downloads': downloads}),
            ('data-download/nominations.html', {'submitted_projects': submitted_projects}),
            ('data-download/award_votes.html', {'nomination_votes': nomination_votes}),
            ('data-download/bans.html', {'bans': bans}),
            ('data-download/showcased_models.html', {'showcased_models': showcased_models}),
            ('data-download/builds.html', {'builds': builds}),
            ('data-download/kit_reviews.html', {'reviews': reviews}),
            # ('data-download/kit_review_votes.html', {'review_votes': review_votes}),
            ('data-download/tracking.html', {'tracked_users': tracked_user}),
            ('data-download/download_requests.html', {'data_downloads': data_downloads}),
        )

        for template_name, context in templates_and_data:
            filename = os.path.split(template_name)[1]
            path = os.path.join(self.tempdir, filename)
            with open(path, 'w') as outfile:
                context['user'] = self.download_request.user
                rendered = render_to_string(template_name, context)
                outfile.write(rendered.encode('utf-8'))

        self.copy_files(photos, 'image')

    def copy_files(self, queryset, field):
        for obj in queryset:
            filefield = getattr(obj, field)
            source = filefield.storage.path(filefield)
            target = os.path.join(self.tempdir, 'files', filefield.name)
            target_dir = os.path.dirname(target)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            try:
                shutil.copy(source, target)
            except IOError:
                pass

    def email(self):
        pass


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
