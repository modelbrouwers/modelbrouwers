from django.conf import settings
from django.test import TestCase
from django.urls import reverse_lazy

from brouwers.users.tests.factories import UserFactory

LIST_URL = reverse_lazy("shop:order-list")


class OrderListTests(TestCase):
    def test_anonymous_user(self):
        response = self.client.get(LIST_URL)

        login_url = f"{settings.LOGIN_URL}?next={LIST_URL}"
        self.assertRedirects(response, login_url)

    def test_authenticated_but_insufficient_permissions(self):
        users = (
            UserFactory.create(),
            UserFactory.create(is_staff=True),
        )
        for user in users:
            with self.subTest(is_staff=user.is_staff):
                self.client.force_login(user=user)

                response = self.client.get(LIST_URL)

                self.assertEqual(response.status_code, 403)

    def test_sufficient_permissions(self):
        user = UserFactory.create(permissions=["shop.change_order"])
        self.client.force_login(user)

        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, 200)
