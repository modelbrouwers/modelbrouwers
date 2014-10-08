""" Test related to navigating the albums pages """
import tempfile
import os
import shutil

from django.conf import settings
from django.test import TestCase

from users.tests.factory_models import UserFactory
from .factory_models import AlbumFactory, PhotoFactory


class DownloadTests(TestCase):
    def setUp(self):
        """ Create a temporary directory for files """
        self.temp_dir = tempfile.mkdtemp()
        self.extract_path = os.path.join(self.temp_dir, 'extracted')
        os.makedirs(self.extract_path)
        self.test_file = os.path.join(os.path.dirname(__file__), 'files/users.png')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_zip_download(self):
        """ Test that zipfiles are correctly generated and downloaded """
        with self.settings(MEDIA_ROOT=self.temp_dir):
            # create the necessary objects
            user = UserFactory()
            album = AlbumFactory(user=user)

            # create directories to copy the files to
            rel_path = os.path.join('albums', str(album.user_id), str(album.id))
            album_path = os.path.join(settings.MEDIA_ROOT, rel_path)
            os.makedirs(album_path)

            for i in range(2):
                new_file = os.path.split(self.test_file)[1]
                filename, ext = os.path.splitext(new_file)
                filename = '{0}-{1}{2}'.format(filename, i, ext)

                dest = os.path.join(album_path, filename)
                shutil.copyfile(self.test_file, dest)
                path = os.path.join(rel_path, filename)

                PhotoFactory(album=album, user=user, image=path)

            # initialization done... test the zip download
            url = '/albums/album/{0}/download/'.format(album.id)

            # not logged in, not allowed to download
            response = self.client.get(url)
            self.assertRedirects(response, '{0}?next={1}'.format(settings.LOGIN_URL, url))

            # log in
            self.client.login(username=user.username, password='password')

            response = self.client.get(url)
            zf = os.path.join(settings.MEDIA_URL, 'albums', str(album.user_id), str(album.id), '{0}.zip'.format(album.id))
            self.assertRedirects(response, zf)
