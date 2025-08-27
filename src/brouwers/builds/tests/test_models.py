from http.client import HTTPMessage
from io import BytesIO, StringIO
from unittest.mock import patch
from urllib.request import HTTPError

from django.conf import settings
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase, override_settings

from brouwers.forum_tools.tests.factories import TopicFactory
from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.utils.tests import reload_urlconf

from .factories import BuildFactory, BuildPhotoFactory


@override_settings(PHPBB_URL="/forum", PHPBB_POSTS_PER_PAGE=5)
class BuildTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        reload_urlconf()

    def setUp(self):
        self.kits = ModelKitFactory.create_batch(5)
        self.topic = TopicFactory.create()
        self.build = BuildFactory.create(
            kits=self.kits[:2], topic_id=self.topic.pk, topic_start_page=2
        )

    def test_topic_url(self):
        self.assertEqual(
            self.build.topic_url,
            f"/forum/viewtopic.php?t={self.topic.pk}&f={self.topic.forum_id}&start=5",
        )

    def test_topic_url_no_startpage(self):
        topic = TopicFactory.create()
        build = BuildFactory.create(topic_id=topic.pk)
        self.assertEqual(
            build.topic_url,
            f"/forum/viewtopic.php?t={topic.pk}&f={topic.forum_id}",
        )

    def test_topic_url_None(self):
        build = BuildFactory.create()
        self.assertIsNone(build.topic)
        self.assertIsNone(build.topic_url)

    def test_topic_unique(self):
        with self.assertRaises(IntegrityError):
            BuildFactory.create(topic_id=self.topic.pk)


ORANGE_PIXEL = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00"
    b"\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\rI"
    b"DAT\x18Wc\xf8\xbf\x84\xf1?\x00\x06\xee\x02\xa4<\xae\x13\xe6\x00\x00\x00\x00IEND"
    b"\xaeB`\x82"
)


class BuildPhotoThumbnailTests(TestCase):
    def setUp(self):
        super().setUp()
        self.addCleanup(
            lambda: call_command(
                "thumbnail", "clear_delete_all", stdout=StringIO(), stderr=StringIO()
            )
        )

    def test_album_photo(self):
        build_photo = BuildPhotoFactory(with_album_photo=True)
        imagefield = build_photo.photo.image
        self.addCleanup(lambda: imagefield.storage.delete(imagefield.name))

        with self.subTest("thumbnail"):
            thumbnail = build_photo.image_thumbnail

            # real generated thumbnail
            self.assertTrue(thumbnail.startswith(settings.MEDIA_URL))

        with self.subTest("preview"):
            preview = build_photo.preview_image

            self.assertTrue(preview.startswith(settings.MEDIA_URL))

    @patch("sorl.thumbnail.images.urlopen")
    def test_photo_url(self, mock_urlopen):
        mock_urlopen.side_effect = (BytesIO(ORANGE_PIXEL), BytesIO(ORANGE_PIXEL))
        build_photo = BuildPhotoFactory(with_photo_url=True)

        with self.subTest("thumbnail"):
            thumbnail = build_photo.image_thumbnail

            # real generated thumbnail
            self.assertTrue(thumbnail.startswith(settings.MEDIA_URL))

        with self.subTest("preview"):
            preview = build_photo.preview_image

            self.assertTrue(preview.startswith(settings.MEDIA_URL))

        mock_urlopen.assert_called()
        self.assertEqual(mock_urlopen.call_count, 2)

    @patch("sorl.thumbnail.images.urlopen")
    def test_photo_is_gone(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("computer says no")
        build_photo = BuildPhotoFactory(with_photo_url=True)

        with self.subTest("thumbnail"):
            thumbnail = build_photo.image_thumbnail

            # real generated thumbnail
            self.assertTrue(thumbnail.startswith(settings.STATIC_URL))

        with self.subTest("preview"):
            preview = build_photo.preview_image

            self.assertTrue(preview.startswith(settings.STATIC_URL))

        mock_urlopen.assert_called()
        self.assertEqual(mock_urlopen.call_count, 1)

    def test_photo_download_404(self):
        build_photo = BuildPhotoFactory(with_photo_url=True)

        with patch(
            "brouwers.builds.models.get_thumbnail",
            side_effect=HTTPError(
                "http://dummy", 404, "Not Found", HTTPMessage(), None
            ),
        ):
            thumbnail = build_photo.image_thumbnail

        self.assertTrue(thumbnail.startswith(settings.STATIC_URL))
