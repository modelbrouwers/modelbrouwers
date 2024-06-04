from django.conf import settings
from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ...constants import OrderStatuses
from ..factories import OrderFactory

DASHBOARD_URL = reverse_lazy("shop:dashboard")


class AccessTests(TestCase):
    def test_anonymous_user(self):
        response = self.client.get(DASHBOARD_URL)

        login_url = f"{settings.LOGIN_URL}?next={DASHBOARD_URL}"
        self.assertRedirects(response, login_url)

    def test_authenticated_but_insufficient_permissions(self):
        users = (
            UserFactory.create(),
            UserFactory.create(is_staff=True),
        )
        for user in users:
            with self.subTest(is_staff=user.is_staff):
                self.client.force_login(user=user)

                response = self.client.get(DASHBOARD_URL)

                self.assertEqual(response.status_code, 403)

    def test_sufficient_permissions(self):
        user = UserFactory.create(permissions=["shop.change_order"])
        self.client.force_login(user)

        response = self.client.get(DASHBOARD_URL)

        self.assertEqual(response.status_code, 200)


class FunctionalDashboardTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = UserFactory.create(superuser=True)

    def test_displays_number_of_new_orders(self):
        OrderFactory.create_batch(4, status=OrderStatuses.received)
        OrderFactory.create_batch(2, status=OrderStatuses.cancelled)
        OrderFactory.create_batch(3, status=OrderStatuses.processing)
        OrderFactory.create_batch(3, status=OrderStatuses.shipped)

        dashboard_page = self.app.get(DASHBOARD_URL, user=self.user)

        tile_text = _("Orders (%(new_order_count)s new)") % {"new_order_count": 4}
        self.assertContains(dashboard_page, tile_text)
