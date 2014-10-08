from django.test import TestCase

from .factory_models import AlbumFactory, PhotoFactory
from users.tests.factory_models import UserFactory


class AlbumTests(TestCase):
    """ Test the (custom) Album model methods """

    def setUp(self):
        self.user = UserFactory.create()

    def test_album_clean_title(self):
        album = AlbumFactory.build(title='foo', trash=False, user=self.user)
        self.assertEquals(album.clean_title, '')
        album.save()
        self.assertEquals(album.clean_title, album.title)

        # trash it
        original_title = album.title
        album.trash = True
        album.save()
        self.assertEquals(album.clean_title, original_title)

    def test_get_cover(self):
        album = AlbumFactory.create()
        self.assertIsNone(album.get_cover())

        photos = PhotoFactory.create_batch(3, album=album, user=album.user)
        album.cover = photos[0]

        self.assertEquals(album.get_cover(), photos[0])

        album.cover = None
        cover = album.get_cover()
        self.assertIn(cover, photos)
        self.assertEquals(album.cover, cover)

    def test_number_of_photos(self):
        album = AlbumFactory.create()
        PhotoFactory.create_batch(2, album=album)
        PhotoFactory.create(album=album, trash=True)

        self.assertEquals(album.number_of_photos(), 2)

    def test_set_order(self):
        AlbumFactory.create(order=1, user=self.user)
        AlbumFactory.create(order=3, user=self.user)
        album = AlbumFactory.create(user=self.user)

        self.assertEquals(album.order, 1)
        album.set_order()
        self.assertEquals(album.order, 4)


class PhotoTests(TestCase):
    """ Test the (custom) Photo model methods """

    def setUp(self):
        self.photo = PhotoFactory.create()

    def test_get_next(self):
        album = AlbumFactory.create()

        # all photos have order = 1
        photos = PhotoFactory.create_batch(5, album=album)
        for i, photo in enumerate(photos):
            if (i+1) == len(photos):
                continue
            expected_next = photos[i+1]
            self.assertEquals(photo.get_next(), expected_next)
