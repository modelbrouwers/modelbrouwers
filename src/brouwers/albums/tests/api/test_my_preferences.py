from django.core.cache import cache
from django.urls import reverse

from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory
from ...models import Preferences
from ...serializers import PreferencesSerializer


class PreferencesTests(APITestCase):

    def setUp(self):
        super(PreferencesTests, self).setUp()
        self.user = UserFactory.create()
        cache.clear()

    def test_preferences(self):
        """
        Ensure we can retrieve the album preferences.
        """
        url = reverse('api:preferences-list')
        url_detail = reverse('api:preferences-detail', kwargs={'pk': 'self'})

        # anonymous
        response = self.client.get(url)
        self.assertEqual(response.data, [])
        response = self.client.get(url_detail)
        self.assertEqual(response.data, PreferencesSerializer(Preferences()).data)

        # authenticated
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(url_detail)
        self.assertEqual(response.data['id'], self.user.preferences.id)
        self.assertEqual(response.data['user'], self.user.pk)

        user2 = UserFactory.create()
        Preferences.objects.get_for(user2)

        self.assertEqual(Preferences.objects.count(), 2)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.user.preferences.id)
