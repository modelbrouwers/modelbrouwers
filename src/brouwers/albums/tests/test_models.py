from django.test import TestCase

from brouwers.users.tests.factory_models import UserFactory
from .factories import AlbumFactory, PhotoFactory


class CategoryTests(TestCase):
    def test_unicode(self):
        album = AlbumFactory.create()
        self.assertEquals(unicode(album.category), album.category.name)


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
                expected_next = None
            else:
                expected_next = photos[i+1]
            self.assertEquals(photo.get_next(), expected_next)

        # test with different orders
        photos[-1].order = 2
        photos[-1].save()

        self.assertEquals(photos[0].get_next(), photos[-1])

    def test_get_prev(self):
        album = AlbumFactory.create()

        # all photos have order = 1
        photos = PhotoFactory.create_batch(5, album=album)
        photos.reverse()
        for i, photo in enumerate(photos):
            if (i+1) == len(photos):
                expected_prev = None
            else:
                expected_prev = photos[i+1]
            self.assertEquals(photo.get_previous(), expected_prev)

        # test with different orders
        photos[-1].order = 0
        photos[-1].save()

        self.assertEquals(photos[0].get_previous(), photos[-1])

    def test_get_next_previous_3(self):
        album = AlbumFactory.create()

        photos = PhotoFactory.create_batch(4, album=album)
        self.assertEquals(list(photos[0].get_next_3()), photos[1:4])
        previous = photos[0:3]
        previous.reverse()
        self.assertEquals(list(photos[-1].get_previous_3()), previous)
