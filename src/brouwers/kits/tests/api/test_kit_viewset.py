from __future__ import absolute_import, unicode_literals

import tempfile

from django.test import override_settings
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory

from ..factories import BoxartFactory, BrandFactory, ScaleFactory
from ...models import Boxart, ModelKit


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class ModelKitTests(APITestCase):

    def test_submit_with_boxart(self):
        brand = BrandFactory.create()
        scale = ScaleFactory.create()
        boxart = BoxartFactory.create()

        user = UserFactory.create()
        self.client.force_login(user, backend='django.contrib.auth.backends.ModelBackend')

        url = reverse('api:modelkit-list')

        response = self.client.post(url, {
            'box_image_uuid': boxart.uuid,
            'brand': brand.pk,
            'difficulty': "30",
            'kit_number': "",
            'name': "F-4F Phantom II",
            'scale': scale.pk,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        kit = ModelKit.objects.get()
        self.assertEqual(kit.brand, brand)
        self.assertEqual(kit.scale, scale)
        self.assertEqual(kit.box_image, boxart.image)

        self.assertFalse(Boxart.objects.exists())
