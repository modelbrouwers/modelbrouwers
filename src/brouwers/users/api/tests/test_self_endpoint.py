from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ...tests.factories import UserFactory


class UserSelfTests(APITestCase):
    def test_not_authenticated(self):
        url = reverse("api:user-profile")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in(self):
        user = UserFactory.create(username="John Wick")
        self.client.force_authenticate(user=user)
        url = reverse("api:user-profile")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "John Wick")
