from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory

from ..factories import AlbumFactory, AlbumGroupFactory


class MyAlbumTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()

    def test_unpaginated_albums(self):
        """
        Ensure we can retrieve a list of our own albums and albums
        accessible via album groups.
        """

        albums = [AlbumFactory.create(user=self.user)]
        AlbumFactory.create(user=self.user, trash=True)
        albums += [AlbumGroupFactory.create(users=[self.user]).album]
        AlbumFactory.create()

        url = reverse('api:my/albums-list')

        # check as anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

        # authenticated
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ensure pagination is disabled
        self.assertNotIn('count', response.data)

        for album, result in zip(albums, response.data):
            self.assertEqual(result['id'], album.id)
            self.assertEqual(result['title'], album.title)
            self.assertEqual(result['description'], album.description)
            self.assertEqual(result['public'], album.public)
            self.assertEqual(result['topic'], album.topic)
            self.assertEqual(result['user'], {'username': album.user.username})
