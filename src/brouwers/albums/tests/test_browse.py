""" Test related to navigating the albums pages """
from django.conf import settings
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from brouwers.users.tests.factory_models import UserFactory
from .factory_models import AlbumFactory, PhotoFactory


class DownloadTests(WebTest):

    def test_zip_download(self):
        """ Test that zipfiles are correctly generated and downloaded """
        # create the necessary objects
        user = UserFactory()
        album = AlbumFactory(user=user)
        PhotoFactory.create_batch(2, album=album, user=user)

        url = reverse('albums:download', kwargs={'pk': album.pk})

        # anonymous
        response = self.app.get(url)
        self.assertRedirects(response, '{0}?next={1}'.format(settings.LOGIN_URL, url))

        # logged in
        response = self.app.get(url, user=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('X-Accel-Redirect', response.headers)  # X-SendFile
        self.assertEqual(len(response.content), 0, 'Body is not empty')


class ViewTests(WebTest):

    def setUp(self):
        self.albums = AlbumFactory.create_batch(3)
        for album in self.albums:
            PhotoFactory.create_batch(3, album=album)

    def test_homepage(self):
        albums_home = self.app.get(reverse('albums:index'))
        self.assertEquals(albums_home.status_code, 200)

        expected_albums = [repr(album) for album in self.albums]
        expected_albums.reverse()
        self.assertQuerysetEqual(albums_home.context['albums'], expected_albums)

        for album in self.albums:
            self.assertIn(album.get_absolute_url(), albums_home)
