""" Test related to navigating the albums pages """
from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from brouwers.users.tests.factory_models import UserFactory
from .factory_models import AlbumFactory, PhotoFactory


class DownloadTests(TestCase):

    def test_zip_download(self):
        """ Test that zipfiles are correctly generated and downloaded """
        # create the necessary objects
        user = UserFactory()
        album = AlbumFactory(user=user)

        PhotoFactory.create_batch(2, album=album, user=user)

        # initialization done... test the zip download
        url = '/albums/album/{0}/download/'.format(album.id)

        # not logged in, not allowed to download
        response = self.client.get(url)
        self.assertRedirects(response, '{0}?next={1}'.format(settings.LOGIN_URL, url))

        # log in
        self.client.login(username=user.username, password='password')

        response = self.client.get(url)
        zf = '{0}albums/{1}/{2}/{2}.zip'.format(settings.MEDIA_URL, album.user_id, album.id)
        self.assertRedirects(response, zf, target_status_code=404)


class ViewTests(WebTest):

    def setUp(self):
        self.albums = AlbumFactory.create_batch(3)
        for album in self.albums:
            PhotoFactory.create_batch(3, album=album)

    def test_homepage(self):
        albums_home = self.app.get(reverse('brouwers.albums.views.index'))
        self.assertEquals(albums_home.status_code, 200)

        expected_albums = [repr(album) for album in self.albums]
        expected_albums.reverse()
        self.assertQuerysetEqual(albums_home.context['albums'], expected_albums)

        for album in self.albums:
            self.assertIn(album.get_absolute_url(), albums_home)
