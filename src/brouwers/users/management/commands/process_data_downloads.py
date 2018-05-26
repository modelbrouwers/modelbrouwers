import os
import shutil
import tempfile
from zipfile import ZipFile

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Prefetch
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

import html2text

from brouwers.builds.models import BuildPhoto

from ...models import DataDownloadRequest


class DataDownload(object):
    def __init__(self, download_request):
        self.download_request = download_request
        self.tempdir = tempfile.mkdtemp(dir=settings.PRIVATE_MEDIA_ROOT)
        self.filename = "{}.zip".format(self.tempdir)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()

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
        self.archive()

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

    def cleanup(self):
        shutil.rmtree(self.tempdir)
        os.remove(self.filename)

    def archive(self):
        with ZipFile(self.filename, 'w', allowZip64=True) as zipfile:
            for dir_path, dirs, files in os.walk(self.tempdir):
                for fn in files:
                    full_path = os.path.join(dir_path, fn)
                    arcname = os.path.relpath(full_path, self.tempdir)
                    zipfile.write(full_path, arcname=arcname)

        with open(self.filename, 'rb') as zipfile:
            self.download_request.zip_file.save(
                os.path.basename(self.filename), File(zipfile)
            )

    def email(self):
        site = Site.objects.get_current()
        user = self.download_request.user
        context = {
            'domain': site.domain,
            'user': user,
            'request': self.download_request,
        }
        html = render_to_string('data-download/mail_ready.html', context)
        message = html2text.html2text(html)
        send_mail(
            _("[Modelbrouwers.nl] Your data download is ready"),
            message, settings.DEFAULT_FROM_EMAIL, [user.email],
            html_message=html
        )


class Command(BaseCommand):
    help = "Process the pending data download requests"

    def handle(self, **options):
        open_requests = (
            DataDownloadRequest.objects
            .select_related('user')
            .filter(finished__isnull=True)
        )
        for download_request in open_requests:
            with DataDownload(download_request) as download:
                download.process()
