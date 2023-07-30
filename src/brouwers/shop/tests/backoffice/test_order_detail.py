from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ..factories import OrderFactory


class OrderDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.order = OrderFactory.create()
        cls.detail_url = reverse(
            "shop:order-detail", kwargs={"reference": cls.order.reference}
        )

    def test_anonymous_user(self):
        response = self.client.get(self.detail_url)

        login_url = f"{settings.LOGIN_URL}?next={self.detail_url}"
        self.assertRedirects(response, login_url)

    def test_authenticated_but_insufficient_permissions(self):
        users = (
            UserFactory.create(),
            UserFactory.create(is_staff=True),
        )
        for user in users:
            with self.subTest(is_staff=user.is_staff):
                self.client.force_login(user=user)

                response = self.client.get(self.detail_url)

                self.assertEqual(response.status_code, 403)

    def test_sufficient_permissions(self):
        user = UserFactory.create(permissions=["shop.change_order"])
        self.client.force_login(user)

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)


class FunctionalOrderDetailTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = UserFactory.create(superuser=True)

    def test_order_reference_shown(self):
        OrderFactory.create(reference="MB-1234")
        detail_url = reverse("shop:order-detail", kwargs={"reference": "MB-1234"})

        response = self.app.get(detail_url, user=self.user)

        self.assertContains(response, "MB-1234")
