import tempfile
import uuid

from django.test import override_settings
from django.urls import reverse
from django.utils.translation import ugettext as _

from rest_framework import status
from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory

from ...models import Boxart, ModelKit
from ..factories import BoxartFactory, BrandFactory, ModelKitFactory, ScaleFactory


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ModelKitTests(APITestCase):
    def test_serialized_output(self):
        kit = ModelKitFactory.create()
        url = reverse("api:modelkit-detail", kwargs={"pk": kit.pk})
        response = self.client.get(url)
        self.assertNotIn("url_kitreviews", response.data)

    def test_submit_without_boxart(self):
        brand = BrandFactory.create()
        scale = ScaleFactory.create()

        user = UserFactory.create()
        self.client.force_login(
            user, backend="django.contrib.auth.backends.ModelBackend"
        )

        url = reverse("api:modelkit-list")

        response = self.client.post(
            url,
            {
                "brand": brand.pk,
                "difficulty": "30",
                "kit_number": "",
                "name": "F-4F Phantom II",
                "scale": scale.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("url_kitreviews", response.data)

        kit = ModelKit.objects.get()
        self.assertEqual(kit.brand, brand)
        self.assertEqual(kit.scale, scale)

    def test_submit_with_boxart(self):
        brand = BrandFactory.create()
        scale = ScaleFactory.create()
        boxart = BoxartFactory.create()

        user = UserFactory.create()
        self.client.force_login(
            user, backend="django.contrib.auth.backends.ModelBackend"
        )

        url = reverse("api:modelkit-list")

        response = self.client.post(
            url,
            {
                "box_image_uuid": boxart.uuid,
                "brand": brand.pk,
                "difficulty": "30",
                "kit_number": "",
                "name": "F-4F Phantom II",
                "scale": scale.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        kit = ModelKit.objects.get()
        self.assertEqual(kit.brand, brand)
        self.assertEqual(kit.scale, scale)
        self.assertEqual(kit.box_image, boxart.image)

        self.assertFalse(Boxart.objects.exists())

    def test_no_boxart_exists(self):
        brand = BrandFactory.create()
        scale = ScaleFactory.create()

        user = UserFactory.create()
        self.client.force_login(
            user, backend="django.contrib.auth.backends.ModelBackend"
        )

        url = reverse("api:modelkit-list")

        response = self.client.post(
            url,
            {
                "box_image_uuid": str(uuid.uuid4()),
                "brand": brand.pk,
                "difficulty": "30",
                "kit_number": "",
                "name": "F-4F Phantom II",
                "scale": scale.pk,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["box_image_uuid"], [_("Invalid upload specified")]
        )
        self.assertFalse(ModelKit.objects.exists())
