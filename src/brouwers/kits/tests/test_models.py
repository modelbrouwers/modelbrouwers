from unittest import mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from .factories import ModelKitFactory, ScaleFactory


class ModelTests(TestCase):
    def test_scale(self):
        scale = ScaleFactory.create(scale=72)
        self.assertEqual(str(scale), "1:72")

    @mock.patch("brouwers.kits.models.ModelKit.full_clean")
    def test_kit_full_clean_called(self, mock):
        ModelKitFactory.create()
        self.assertEqual(mock.call_count, 1)

    def test_kit_full_clean_not_called_existing_record(self):
        kit = ModelKitFactory.create()
        with mock.patch("brouwers.kits.models.ModelKit.full_clean") as mocked:
            kit.save()
            self.assertFalse(mocked.called)

    def test_kit_str(self):
        kit = ModelKitFactory.create(name=u"😻", brand__name=u"SMĚR")
        self.assertEqual(str(kit), u"SMĚR - 😻")

    def test_duplicate_kitnumber(self):
        with self.assertRaises(ValidationError):
            ModelKitFactory.create_batch(
                2, brand__name=u"SMĚR", kit_number="012345", scale__scale=144
            )

    def test_has_box_image(self):
        kit = ModelKitFactory.build(box_image="")
        self.assertFalse(kit.has_box_image())

        kit2 = ModelKitFactory.build(box_image="non-existant.jpg")
        self.assertFalse(kit2.has_box_image())

        kit3 = ModelKitFactory.create()
        self.assertTrue(kit3.has_box_image())
