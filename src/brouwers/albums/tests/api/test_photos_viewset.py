import tempfile

from django.urls import reverse

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory

from ..factories import AlbumFactory, PhotoFactory


class PhotoViewsetTests(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()
        self.album = AlbumFactory.create(user=self.user)
        self.list_url = reverse("api:photo-list")

    def test_upload(self):
        """
        Test that API uploads are possible.
        """
        data = {"album": self.album.pk}

        # anonymous
        response = self.client.post(self.list_url, data, format="multipart")
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

        # authenticated
        self.client.login(username=self.user.username, password="password")

        # create an image
        image = Image.new("RGB", (192, 108), "green")
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file, format="JPEG")

        with open(tmp_file.name, "rb") as image:
            data.update(
                {
                    "image": image,
                    "description": "dummy description",
                }
            )
            response = self.client.post(self.list_url, data, format="multipart")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["success"], True)

    def test_failing_upload(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            self.list_url, {"album": self.album.pk}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("image", response.data)  # there must be an error

    def test_list_photos(self):
        photos = PhotoFactory.create_batch(10, album=self.album)
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(self.list_url, {"album": self.album.pk})
        self.assertEqual(response.data["count"], 10)
        for photo, result in zip(photos, response.data["results"]):
            self.assertEqual(photo.id, result["id"])
            self.assertEqual(set(result["image"].keys()), set(["large", "thumb"]))

    def test_unauthenticated_rotate(self):
        photo = PhotoFactory.create(
            album=self.album, image__width=100, image__height=50
        )
        detail_url = reverse("api:photo-rotate", kwargs={"pk": photo.pk})
        response = self.client.patch(detail_url, data={"direction": "cw"})
        self.assertEqual(response.status_code, 403)

    def test_rotate(self):
        photo = PhotoFactory.create(
            album=self.album, image__width=100, image__height=50
        )
        self.client.login(username=self.user.username, password="password")
        detail_url = reverse("api:photo-rotate", kwargs={"pk": photo.pk})

        response = self.client.patch(detail_url, data={"direction": "cw"})  # clockwise
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["width"], 50)
        self.assertEqual(response.data["height"], 100)
        with Image.open(photo.image.path) as img:
            self.assertEqual(img.size, (50, 100))

        response = self.client.patch(
            detail_url, data={"direction": "ccw"}
        )  # counter-clockwise
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["width"], 100)
        self.assertEqual(response.data["height"], 50)
        with Image.open(photo.image.path) as img:
            self.assertEqual(img.size, (100, 50))

    def test_invalid_rotate(self):
        photo = PhotoFactory.create(
            album=self.album, image__width=100, image__height=50
        )
        self.client.login(username=self.user.username, password="password")
        detail_url = reverse("api:photo-rotate", kwargs={"pk": photo.pk})
        response = self.client.patch(
            detail_url, data={"direction": "fl;asjdf"}
        )  # clockwise
        self.assertEqual(response.status_code, 400)
