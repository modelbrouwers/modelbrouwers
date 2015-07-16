import tempfile

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image

from brouwers.users.tests.factories import UserFactory
from ..factories import AlbumFactory, PhotoFactory


class PhotoViewsetTests(APITestCase):

    def setUp(self):
        super(PhotoViewsetTests, self).setUp()
        self.user = UserFactory.create()
        self.album = AlbumFactory.create(user=self.user)
        self.list_url = reverse('api:photo-list')

    def test_upload(self):
        """
        Test that API uploads are possible.
        """
        data = {'album': self.album.pk}

        # anonymous
        response = self.client.post(self.list_url, data, format='multipart')
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})

        # authenticated
        self.client.login(username=self.user.username, password='password')

        # create an image
        image = Image.new('RGB', (192, 108), 'green')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='JPEG')

        with open(tmp_file.name, 'rb') as image:
            data.update({
                'image': image,
                'description': 'dummy description',
            })
            response = self.client.post(self.list_url, data, format='multipart')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['success'], True)

    def test_failing_upload(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(self.list_url, {'album': self.album.pk}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('image', response.data)  # there must be an error

    def test_list_photos(self):
        photos = PhotoFactory.create_batch(10, album=self.album)
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.list_url, {'album': self.album.pk})
        self.assertEqual(response.data['count'], 10)
        for photo, result in zip(photos, response.data['results']):
            self.assertEqual(photo.id, result['id'])
            self.assertEqual(set(result['image'].keys()), set(['large', 'thumb']))

    # def test_detail_next_previous(self):
    #     pass  # TODO

    def test_rotate(self):
        photo = PhotoFactory.create(album=self.album, image__width=100, image__height=50)
        self.client.login(username=self.user.username, password='password')
        detail_url = reverse('api:photo-rotate', kwargs={'pk': photo.pk})
        response = self.client.post(detail_url, {'direction': 'cw'})  # clockwise
