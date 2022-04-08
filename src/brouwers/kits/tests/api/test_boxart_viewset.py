import tempfile

from django.test import override_settings
from django.urls import reverse

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory

from ...models import Boxart


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BoxartTests(APITestCase):
    def test_upload_endpoint(self):
        user = UserFactory.create()
        self.client.force_login(
            user, backend="django.contrib.auth.backends.ModelBackend"
        )

        url = reverse("api:boxart-list")

        # create an image
        image = Image.new("RGB", (10, 10), "green")
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file, format="JPEG")

        with open(tmp_file.name, "rb") as image:
            response = self.client.post(url, {"image": image}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        boxart = Boxart.objects.get()
        self.assertEqual(
            response.data,
            {
                "uuid": boxart.uuid,
                "image": "http://testserver{}".format(boxart.image.url),
                "success": True,
            },
        )
