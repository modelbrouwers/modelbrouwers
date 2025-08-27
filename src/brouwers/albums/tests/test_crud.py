from django.urls import reverse
from django.utils.translation import gettext_lazy as _

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
        super().setUp()
        self.user = UserFactory.create()

    def test_album_create(self):
        self.assertEqual(Album.objects.count(), 0)
        url = reverse("albums:create")
        self._test_login_required(url)

        topic = TopicFactory.create()

        create = self.app.get(url, user=self.user)
        self.assertEqual(create.status_code, 200)
        form = create.forms["album-form"]
        form["title"] = "My first album"
        form["description"] = "Dummy description"
        form["topic"] = (
            "http://modelbrouwers.nl/phpBB3/viewtopic.php"
            f"?f={topic.forum_id}&t={topic.topic_id}"
        )

        response = form.submit()

        self.assertEqual(Album.objects.count(), 1)
        album = Album.objects.first()
        redirect = "{}?album={}".format(reverse("albums:upload"), album.id)
        self.assertRedirects(response, redirect)

        self.assertEqual(album.topic, topic)
        self.assertEqual(album.title, "My first album")
        self.assertEqual(album.description, "Dummy description")

    def test_album_create_same_title(self):
        url = reverse("albums:create")
        create = self.app.get(url, user=self.user)
        self.assertEqual(create.status_code, 200)
        form = create.forms["album-form"]
        form["title"] = "My album"

        response = form.submit()
        self.assertEqual(Album.objects.count(), 1)

        # submit again
        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "title",
            errors=[str(_("You already have an album with this title."))],
        )

    def test_preferences_update(self):
        url = reverse("albums:settings")
        self._test_login_required(url)

        preferences = self.app.get(url, user=self.user)
        self.assertEqual(preferences.status_code, 200)
        form = preferences.forms["preferences-form"]
        response = form.submit()
        self.assertRedirects(response, reverse("albums:index"))


class UploadTests(LoginRequiredMixin, WebTest):
    url = reverse("albums:upload")

    def setUp(self):
        super().setUp()
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
        self.assertRedirects(response, reverse("albums:create"))

    def test_uploadview(self):
        """
        Given that the user has at least one album, assert that the upload
        page is accessible.
        """
        AlbumFactory.create()  # random user
        album = AlbumFactory.create(user=self.user)
        upload = self.app.get(self.url, user=self.user)
        self.assertEqual(upload.status_code, 200)

        uploadform = upload.context["form"]
        self.assertQuerySetEqual(
            uploadform.fields["album"].queryset, [repr(album)], transform=repr
        )
