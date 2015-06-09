from django.core.urlresolvers import reverse

from django_webtest import WebTest

from brouwers.forum_tools.tests.factories import TopicFactory
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin
from ..models import Album
from .factories import AlbumFactory


class CrudTests(LoginRequiredMixin, WebTest):
    """
    Test the create-read-update-delete views.
    """

    def setUp(self):
        super(CrudTests, self).setUp()
        self.user = UserFactory.create()

    def test_album_create(self):
        self.assertEqual(Album.objects.count(), 0)
        url = reverse('albums:create')
        self._test_login_required(url)

        topic = TopicFactory.create()

        create = self.app.get(url, user=self.user)
        self.assertEqual(create.status_code, 200)
        create.form['title'] = 'My first album'
        create.form['description'] = 'Dummy description'
        create.form['topic'] = 'http://modelbrouwers.nl/phpBB3/viewtopic.php?f=%d&t=%d' % (
            topic.forum_id, topic.topic_id)

        response = create.form.submit()

        self.assertEqual(Album.objects.count(), 1)
        album = Album.objects.first()
        redirect = u"{}?album={}".format(reverse('albums:upload'), album.id)
        self.assertRedirects(response, redirect)

        self.assertEqual(album.topic, topic)
        self.assertEqual(album.title, 'My first album')
        self.assertEqual(album.description, 'Dummy description')

    def test_preferences_update(self):
        url = reverse('albums:settings')
        self._test_login_required(url)

        preferences = self.app.get(url, user=self.user)
        self.assertEqual(preferences.status_code, 200)
        response = preferences.form.submit()
        self.assertRedirects(response, reverse('albums:index'))


class UploadTests(LoginRequiredMixin, WebTest):

    url = reverse('albums:upload')

    def setUp(self):
        super(UploadTests, self).setUp()
        self.user = UserFactory.create()

    def test_upload_view_anon(self):
        """
        Test that login is required for the upload view.
        """
        self._test_login_required(self.url)

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
