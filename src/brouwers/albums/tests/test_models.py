from django.test import TestCase, override_settings

from sorl.thumbnail.models import KVStore

from brouwers.users.tests.factories import UserFactory

from .factories import AlbumFactory, PhotoFactory


class CategoryTests(TestCase):
    def test_str(self):
        album = AlbumFactory.create()
        self.assertEqual(str(album.category), album.category.name)


class AlbumTests(TestCase):
    """Test the (custom) Album model methods"""

    def setUp(self):
        self.user = UserFactory.create()

    def test_album_clean_title(self):
        album = AlbumFactory.build(
            title="foo", trash=False, user=self.user, category=None
        )
        self.assertEqual(album.clean_title, "")
        album.save()
        self.assertEqual(album.clean_title, album.title)

        # trash it
        original_title = album.title
        album.trash = True
        album.save()
        self.assertEqual(album.clean_title, original_title)

    def test_get_cover(self):
        album = AlbumFactory.create()
        self.assertIsNone(album.get_cover())

        photos = PhotoFactory.create_batch(3, album=album, user=album.user)
        album.cover = photos[0]

        self.assertEqual(album.get_cover(), photos[0])

        album.cover = None
        cover = album.get_cover()
        self.assertIn(cover, photos)
        self.assertEqual(album.cover, cover)

    def test_set_order(self):
        AlbumFactory.create(order=1, user=self.user)
        AlbumFactory.create(order=3, user=self.user)
        album = AlbumFactory.create(user=self.user)

        self.assertEqual(album.order, 1)
        album.set_order()
        self.assertEqual(album.order, 4)


class PhotoTests(TestCase):
    """Test the (custom) Photo model methods"""

    @override_settings(
        THUMBNAIL_KVSTORE="sorl.thumbnail.kvstores.cached_db_kvstore.KVStore"
    )
    def test_thumbs_generated(self):
        """
        Test that the thumbnails are generated in the post_save
        """
        qs = KVStore.objects.all()
        self.assertEqual(qs.count(), 0)
        PhotoFactory.create(image__width=1600, image__height=1200)
        self.assertGreaterEqual(qs.count(), 3)
