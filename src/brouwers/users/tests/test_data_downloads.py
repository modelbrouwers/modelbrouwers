import tempfile
from datetime import timedelta
from io import StringIO
from unittest.mock import patch

from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from django_webtest import WebTest

from brouwers.albums.tests.factories import PhotoFactory

from ..management.commands.process_data_downloads import DataDownload
from ..models import DataDownloadRequest
from .factories import DataDownloadRequestFactory, UserFactory


class ViewTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()

    # requesting a data download

    def test_auth_required(self):
        url = reverse("users:data-download")

        response = self.client.post(url)

        self.assertEqual(response.status_code, 403)

    def test_from_profile_page(self):
        url = reverse("users:profile")
        profile = self.app.get(url, user=self.user)

        response = profile.forms[2].submit()

        self.assertRedirects(response, url)
        download_request = DataDownloadRequest.objects.get()
        self.assertEqual(download_request.user, self.user)
        self.assertIsNone(download_request.finished)
        self.assertIsNone(download_request.downloaded)
        self.assertEqual(download_request.zip_file, "")

    def test_has_pending_request(self):
        DataDownloadRequest.objects.create(user=self.user)

        self.client.force_login(self.user)
        self.client.post(reverse("users:data-download"))

        self.assertEqual(DataDownloadRequest.objects.count(), 1)

    # downloading the generated zip file

    def test_download_prepared_request(self):
        dr = DataDownloadRequestFactory.create(user=self.user, with_file=True)
        self.addCleanup(lambda: dr.zip_file.delete(save=False))

        url = reverse("users:data-download-file", kwargs={"pk": dr.pk})

        download = self.app.get(url, user=self.user)

        self.assertEqual(download.status_code, 200)
        # nginx
        self.assertIn("X-Accel-Redirect", download.headers)

    def test_no_requests(self):
        url = reverse("users:data-download-file", kwargs={"pk": 0})

        download = self.app.get(url, user=self.user, status=404)

        self.assertEqual(download.status_code, 404)

    def test_no_auth(self):
        url = reverse("users:data-download-file", kwargs={"pk": 0})
        redirect_url = "{}?next={}".format(settings.LOGIN_URL, url)

        response = self.client.get(url)

        self.assertRedirects(response, redirect_url, fetch_redirect_response=False)

    def test_download_other_user(self):
        user2 = UserFactory.create()
        dr = DataDownloadRequestFactory.create(user=self.user, with_file=True)
        url = reverse("users:data-download-file", kwargs={"pk": dr.pk})

        response = self.app.get(url, user=user2, status=404)

        self.assertEqual(response.status_code, 404)


class ClearDataDownloadsTests(TestCase):
    def test_command(self):
        dr1 = DataDownloadRequestFactory.create()
        dr2 = DataDownloadRequestFactory.create(with_file=True)
        dr3 = DataDownloadRequestFactory.create(
            with_file=True, downloaded=timezone.now() - timedelta(minutes=30)
        )
        dr4 = DataDownloadRequestFactory.create(
            with_file=True, downloaded=timezone.now() - timedelta(hours=2)
        )

        def cleanup():
            for dr in (dr2, dr3, dr4):
                dr.zip_file.delete(save=False)

        self.addCleanup(cleanup)

        call_command("clear_data_downloads", stdout=StringIO())

        dr1.refresh_from_db()
        self.assertIsNone(dr1.finished)
        self.assertIsNone(dr1.downloaded)
        self.assertEqual(dr1.zip_file, "")

        dr2.refresh_from_db()
        self.assertIsNotNone(dr2.finished)
        self.assertIsNone(dr2.downloaded)
        self.assertNotEqual(dr2.zip_file, "")

        dr3.refresh_from_db()
        self.assertIsNotNone(dr3.finished)
        self.assertIsNotNone(dr3.downloaded)
        self.assertNotEqual(dr3.zip_file, "")

        dr4.refresh_from_db()
        self.assertIsNotNone(dr4.finished)
        self.assertIsNotNone(dr4.downloaded)
        self.assertEqual(dr4.zip_file, "")


class ProcessDataDownloadsTests(TestCase):
    def test_command(self):
        dr1 = DataDownloadRequestFactory.create()
        DataDownloadRequestFactory.create(with_file=True)
        DataDownloadRequestFactory.create(
            with_file=True, downloaded=timezone.now() - timedelta(minutes=30)
        )
        DataDownloadRequestFactory.create(
            with_file=True, downloaded=timezone.now() - timedelta(hours=2)
        )

        with patch(
            "brouwers.users.management.commands.process_data_downloads.DataDownload"
        ) as mock_request:
            call_command("process_data_downloads")

        mock_request.assert_called_once_with(dr1)

    @override_settings(PRIVATE_MEDIA_ROOT=tempfile.mkdtemp())
    def test_data_download(self):
        dr = DataDownloadRequestFactory.create()
        PhotoFactory.create(user=dr.user)
        self.addCleanup(lambda: dr.zip_file.delete(save=False))

        with DataDownload(dr) as download:
            download.process()
            download.email()

        dr.refresh_from_db()
        self.assertNotEqual(dr.zip_file, "")
        self.assertTrue(dr.zip_file.storage.exists(dr.zip_file.name))

        self.assertEqual(len(mail.outbox), 1)
