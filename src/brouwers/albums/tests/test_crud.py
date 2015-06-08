from django.conf import settings
from django.core.urlresolvers import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory
from .factories import AlbumFactory


class CrudTests(WebTest):
    """
    Test the create-read-update-delete views.
    """
    pass


class UploadTests(WebTest):

    url = reverse('albums:upload')

    def setUp(self):
        super(UploadTests, self).setUp()
        self.user = UserFactory.create()

    def test_upload_view_anon(self):
        """
        Test that login is required for the upload view.
        """
        response = self.app.get(self.url)
        redirect = u"{}?next={}".format(settings.LOGIN_URL, self.url)
        self.assertRedirects(response, redirect)

    def test_uploadview_no_albums(self):
        """
        Test that the user is redirected if he/she has no albums yet
        """
        self.assertEqual(self.user.album_set.count(), 0)
        response = self.app.get(self.url, user=self.user)
        self.assertRedirects(response, reverse('albums:create'))

    def test_uploadview(self):
        """
        Given that the user has at least one album, assert that the upload
        page is accessible.
        """
        AlbumFactory.create()  # random user
        album = AlbumFactory.create(user=self.user)
        upload = self.app.get(self.url, user=self.user)
        self.assertEqual(upload.status_code, 200)

        uploadform = upload.context['form']
        self.assertQuerysetEqual(uploadform.fields['album'].queryset, [repr(album)])
