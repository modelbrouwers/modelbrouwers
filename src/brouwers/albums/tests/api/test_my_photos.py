from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory

from ...models import Album
from ..factories import AlbumFactory, AlbumGroupFactory, PhotoFactory
from ..utils import override_preferences


class MyPhotoTests(APITestCase):

    def setUp(self):
        super(MyPhotoTests, self).setUp()
        self.user = UserFactory.create()

    def test_paginated_photos(self):
        """
        Ensure we can retrieve a list of our own photos and photos
        accessible via album groups.
        """

        own_album = AlbumFactory.create(user=self.user)
        photos = PhotoFactory.create_batch(3, album=own_album)
        PhotoFactory.create_batch(2, album=own_album, trash=True)
        trash_album = AlbumFactory.create(user=self.user, trash=True)
        PhotoFactory.create(album=trash_album)
        album_group = AlbumGroupFactory.create(users=[self.user])
        photos += PhotoFactory.create_batch(4, album=album_group.album)
        random_album = AlbumFactory.create()
        PhotoFactory.create_batch(5, album=random_album)

        url = reverse('api:my/photos-list')

        # check as anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

        # authenticated
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure pagination is active
        self.assertEqual(response.data['count'], len(photos))

        photos.reverse()
        results = response.data['results']
        for photo, result in zip(photos, results):
            self.assertEqual(result['id'], photo.id)
            self.assertEqual(result['user'], photo.user_id)
            image = result['image']
            self.assertIn('large', image)
            self.assertIn('thumb', image)

        # test filter
        response = self.client.get(url, {'album': own_album.pk})
        self.assertEqual(response.data['count'], 3)
        results = response.data['results']

        for result, photo in zip(results, photos[-3:]):
            self.assertEqual(result['id'], photo.id)

    def test_custom_pagination(self):
        url = reverse('api:my/photos-list')
        own_album = AlbumFactory.create(user=self.user)
        PhotoFactory.create_batch(4, album=own_album)
        self.client.login(username=self.user.username, password='password')
        with override_preferences(self.user, paginate_by_sidebar=3):
            response = self.client.get(url)
        self.assertEqual(response.data['paginate_by'], 3)

    def test_set_cover(self):
        own_album = AlbumFactory.create(user=self.user)
        photos = PhotoFactory.create_batch(2, album=own_album)

        other_album = AlbumFactory.create()
        other_photos = PhotoFactory.create_batch(2, album=other_album)

        self.assertIsNone(own_album.cover)
        self.assertIsNone(other_album.cover)

        url = reverse('api:my/photos-set-cover', kwargs={'pk': photos[1].pk})

        # check anonymous
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # authenticated
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        album = Album.objects.get(pk=own_album.pk)
        self.assertEqual(album.cover, photos[1])

        # other person album/photo
        url = reverse('api:my/photos-set-cover', kwargs={'pk': other_photos[1].pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
