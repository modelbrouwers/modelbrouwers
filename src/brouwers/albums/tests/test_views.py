from django.conf import settings
from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin

from ..models import Album, Photo
from .factories import AlbumFactory, AlbumGroupFactory, PhotoFactory


class PublicViewTests(WebTest):
    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()

    def test_index(self):
        AlbumFactory.create_batch(13)
        AlbumFactory.create_batch(2, trash=True)
        for i in range(4):
            PhotoFactory.create(album__public=True)
        for i in range(2):
            PhotoFactory.create(album__public=False)
        for i in range(2):
            PhotoFactory.create(trash=True)

        index = self.app.get(reverse("albums:index"))
        self.assertEqual(index.status_code, 200)
        albums = Album.objects.filter(trash=False, public=True).order_by(
            "-last_upload", "-pk"
        )[:12]
        self.assertQuerysetEqual(index.context["albums"], [repr(x) for x in albums])
        photos = Photo.objects.filter(
            trash=False, album__public=True, album__trash=False
        ).order_by("-uploaded")
        self.assertQuerysetEqual(
            index.context["latest_uploads"], [repr(x) for x in photos]
        )

    def test_list(self):
        url = reverse("albums:all")
        albums = AlbumFactory.create_batch(17)
        albums.reverse()
        listview = self.app.get(url)
        self.assertEqual(listview.status_code, 200)
        self.assertQuerysetEqual(
            listview.context["albums"], [repr(x) for x in albums[:16]]
        )

    def test_album_detail(self):
        album = AlbumFactory.create()
        photos = PhotoFactory.create_batch(26, album=album)
        url = reverse("albums:detail", kwargs={"pk": album.pk})
        detail = self.app.get(url)
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.context["album"], album)
        album = detail.context["album"]
        self.assertEqual(album.views, 1)
        self.assertQuerysetEqual(
            detail.context["photos"], [repr(x) for x in photos[:24]]
        )
        self.assertContains(detail, "pagination")

    def test_photo_detail(self):
        photo = PhotoFactory.create()
        url = reverse("albums:photo-detail", kwargs={"pk": photo.pk})
        detail = self.app.get(url)
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.context["photo"], photo)
        photo = detail.context["photo"]
        self.assertEqual(photo.views, 1)

        # more private version
        albumgroup = AlbumGroupFactory.create(users=[self.user])
        photo = PhotoFactory.create(album=albumgroup.album)
        url = reverse("albums:photo-detail", kwargs={"pk": photo.pk})
        detail = self.app.get(url, user=self.user)
        self.assertEqual(detail.status_code, 200)


class DownloadTests(LoginRequiredMixin, WebTest):
    def test_zip_download(self):
        """Test that zipfiles are correctly generated and downloaded"""
        # create the necessary objects
        user = UserFactory.create()
        album = AlbumFactory.create(user=user)
        PhotoFactory.create_batch(2, album=album, user=user)

        url = reverse("albums:download", kwargs={"pk": album.pk})
        self._test_login_required(url)

        # logged in
        response = self.app.get(url, user=user)
        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Accel-Redirect", response.headers)  # X-SendFile
        self.assertEqual(len(response.content), 0, "Body is not empty")


class PrivateViewTests(LoginRequiredMixin, WebTest):
    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()

    def test_my_albums(self):
        url = reverse("albums:mine")
        self._test_login_required(url)

        AlbumFactory.create(user=self.user, trash=True)
        album1 = AlbumFactory.create(user=self.user, public=True)
        album2 = AlbumFactory.create(user=self.user, public=False)
        albumgroup1 = AlbumGroupFactory.create(users=[self.user])
        albumgroup2 = AlbumGroupFactory.create(album__user=self.user)

        my_albums_list = self.app.get(url, user=self.user)
        self.assertEqual(my_albums_list.status_code, 200)

        tabs = my_albums_list.context["tabcontent"]

        self.assertQuerysetEqual(
            tabs["public"], [repr(album1), repr(albumgroup2.album)]
        )
        self.assertQuerysetEqual(tabs["private"], [repr(album2)])
        self.assertQuerysetEqual(tabs["shared-with-me"], [repr(albumgroup1.album)])
        self.assertQuerysetEqual(tabs["shared-by-me"], [repr(albumgroup2.album)])

        # assert that the edit urls are visible
        for album in [album1, album2, albumgroup2.album]:
            edit_url = reverse("albums:update", kwargs={"pk": album.pk})
            self.assertContains(my_albums_list, edit_url)

        # other owner, edit url may not be visible
        edit_url = reverse("albums:update", kwargs={"pk": albumgroup1.album.pk})
        self.assertNotContains(my_albums_list, edit_url)

    def test_update_album(self):
        album = AlbumFactory.create(user=self.user, title="Initial title")
        url_update = reverse("albums:update", kwargs={"pk": album.pk})

        # anonymous user
        detail_page = self.app.get(album.get_absolute_url())
        self.assertEqual(detail_page.status_code, 200)
        self.assertNotContains(detail_page, url_update)
        # try it anyway
        update_page = self.app.get(url_update)
        expected_redirect = u"%s?next=%s" % (settings.LOGIN_URL, url_update)
        self.assertRedirects(update_page, expected_redirect)

        # other user
        other_user = UserFactory.create()
        self.assertNotEqual(album.user, other_user)
        update_page = self.app.get(url_update, user=other_user, status=404)

        # album owner
        update_page = self.app.get(url_update, user=self.user, status=200)
        update_page.form["title"] = "New title"
        update_page.form.submit().follow()

        album = Album.objects.get(pk=album.pk)
        self.assertEqual(album.title, "New title")

    def test_delete_album(self):
        album = AlbumFactory.create(user=self.user)
        url_delete = reverse("albums:delete", kwargs={"pk": album.pk})

        # anonymous user
        detail_page = self.app.get(album.get_absolute_url(), status=200)
        self.assertNotContains(detail_page, url_delete)
        # try it anyway
        delete_page = self.app.get(url_delete)
        expected_redirect = u"%s?next=%s" % (settings.LOGIN_URL, url_delete)
        self.assertRedirects(delete_page, expected_redirect)

        # other user
        other_user = UserFactory.create()
        self.assertNotEqual(album.user, other_user)
        delete_page = self.app.get(url_delete, user=other_user, status=404)

        # album owner
        delete_page = self.app.get(url_delete, user=self.user, status=200)
        delete_page.form.submit().follow()

        album = Album.objects.get(pk=album.pk)
        self.assertTrue(album.trash)

    def test_restore_album(self):
        album = AlbumFactory.create(user=self.user, title="Album to restore")
        self.assertEqual(album.clean_title, "Album to restore")
        album.trash = True
        album.save()

        url_restore = reverse("albums:restore", kwargs={"pk": album.pk})

        # anonymous user
        self.app.get(album.get_absolute_url(), status=404)
        # try it anyway
        restore_page = self.app.get(url_restore)
        expected_redirect = u"%s?next=%s" % (settings.LOGIN_URL, url_restore)
        self.assertRedirects(restore_page, expected_redirect)

        # other user
        other_user = UserFactory.create()
        self.assertNotEqual(album.user, other_user)
        restore_page = self.app.get(url_restore, user=other_user, status=404)

        # album owner
        restore_page = self.app.get(url_restore, user=self.user, status=200)
        restore_page.form.submit().follow()

        album = Album.objects.get(pk=album.pk)
        self.assertFalse(album.trash)
        self.assertEqual(album.title, "Album to restore")

    def test_delete_photo(self):
        photo = PhotoFactory.create(user=self.user)
        url_delete = reverse("albums:photo_delete", kwargs={"pk": photo.pk})

        # anonymous user
        detail_page = self.app.get(photo.get_absolute_url(), status=200)
        self.assertNotContains(detail_page, url_delete)
        # try it anyway
        delete_page = self.app.get(url_delete)
        expected_redirect = u"%s?next=%s" % (settings.LOGIN_URL, url_delete)
        self.assertRedirects(delete_page, expected_redirect)

        # other user
        other_user = UserFactory.create()
        self.assertNotEqual(photo.user, other_user)
        delete_page = self.app.get(url_delete, user=other_user, status=404)

        # photo owner
        delete_page = self.app.get(url_delete, user=self.user, status=200)
        delete_page.form.submit().follow()

        photo = Photo.objects.get(pk=photo.pk)
        self.assertTrue(photo.trash)

    def test_restore_photo(self):
        photo = PhotoFactory.create(user=self.user)
        photo.trash = True
        photo.save()

        url_restore = reverse("albums:photo_restore", kwargs={"pk": photo.pk})

        # anonymous user
        self.app.get(photo.get_absolute_url(), status=404)
        # try it anyway
        restore_page = self.app.get(url_restore)
        expected_redirect = u"%s?next=%s" % (settings.LOGIN_URL, url_restore)
        self.assertRedirects(restore_page, expected_redirect)

        # other user
        other_user = UserFactory.create()
        self.assertNotEqual(photo.user, other_user)
        restore_page = self.app.get(url_restore, user=other_user, status=404)

        # photo owner
        restore_page = self.app.get(url_restore, user=self.user, status=200)
        restore_page.form.submit().follow()

        photo = Photo.objects.get(pk=photo.pk)
        self.assertFalse(photo.trash)

    def test_update_photo(self):
        albums = AlbumFactory.create_batch(2, user=self.user)
        photo = PhotoFactory.create(
            user=self.user, description="Initial description", album=albums[0]
        )
        url_update = reverse("albums:photo_update", kwargs={"pk": photo.pk})

        # anonymous user
        album_page = self.app.get(photo.album.get_absolute_url(), status=200)
        self.assertNotContains(album_page, url_update)
        detail_page = self.app.get(photo.get_absolute_url(), status=200)
        self.assertNotContains(detail_page, url_update)
        # try it anyway
        update_page = self.app.get(url_update)
        expected_redirect = u"%s?next=%s" % (settings.LOGIN_URL, url_update)
        self.assertRedirects(update_page, expected_redirect)

        # other user
        other_user = UserFactory.create()
        self.assertNotEqual(photo.user, other_user)
        update_page = self.app.get(url_update, user=other_user, status=404)

        # photo owner
        update_page = self.app.get(url_update, user=self.user, status=200)
        update_page.form["description"] = "New description"
        update_page.form["album"] = [str(albums[1].pk)]
        update_page.form.submit().follow()

        photo = Photo.objects.get(pk=photo.pk)
        self.assertEqual(photo.description, "New description")
        self.assertEqual(photo.album, albums[1])
