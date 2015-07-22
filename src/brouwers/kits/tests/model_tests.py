from django.test import TestCase

from .factories import ScaleFactory, ModelKitFactory


class ModelTests(TestCase):

    def test_scale(self):
        scale = ScaleFactory.create(scale=72)
        self.assertEqual(str(scale), '1:72')
