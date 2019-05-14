from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from brouwers.users.tests.factories import UserFactory


class UserProfileApiTest(APITransactionTestCase):
    """
    Test that CRUD operations for products work correctly
    """

    def setUp(self):
        cache.clear()
        self.user = UserFactory.create()  # Creates UserProfile through a signal
        self.client.force_authenticate(user=self.user)
        self.addCleanup(cache.clear)

    def test_get_profile(self):
        profile = self.user.userprofile
        response = self.client.get(reverse('api:user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['id'], profile.pk)
        self.assertEqual(response.data['data']['user']['username'], profile.user.username)

        # Anon user should get 404
        self.client.logout()
        response = self.client.get(reverse('api:user-profile'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
