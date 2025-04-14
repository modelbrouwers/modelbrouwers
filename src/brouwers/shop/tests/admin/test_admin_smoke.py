"""
Smoke tests for the admin.
"""

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse_lazy

from brouwers.users.tests.factories import UserFactory

from ...constants import CartStatuses, DeliveryMethods
from ..factories import (
    CartFactory,
    CartProductFactory,
    OrderFactory,
    PaymentFactory,
    ProductFactory,
    ShippingCostFactory,
)


class BaseAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(superuser=True)

    def setUp(self):
        super().setUp()

        self.client.force_login(self.user)


class ProductAdminSmokeTests(BaseAdminTestCase):
    url = reverse_lazy("admin:shop_product_changelist")

    def test_changelist_render(self):
        ProductFactory.create_batch(10)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_changelist_search_ok(self):
        response = self.client.get(self.url, {"q": "foo"})

        self.assertEqual(response.status_code, 200)


class OrderAdminSmokeTests(BaseAdminTestCase):
    url = reverse_lazy("admin:shop_order_changelist")

    def test_changelist_render(self):
        OrderFactory.create_batch(3)
        PaymentFactory.create_batch(2, is_cancelled=False)
        PaymentFactory.create_batch(2, is_cancelled=True)
        cart = CartFactory.create(status=CartStatuses.closed)
        CartProductFactory.create(cart=cart, amount=1)
        cart.save_snapshot()
        OrderFactory.create(
            cart=cart,
            delivery_method=DeliveryMethods.mail,
            shipping_costs=Decimal("9.95"),
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_changelist_search_ok(self):
        response = self.client.get(self.url, {"q": "foo"})

        self.assertEqual(response.status_code, 200)


class PaymentAdminSmokeTests(BaseAdminTestCase):
    url = reverse_lazy("admin:shop_payment_changelist")

    def test_changelist_render(self):
        PaymentFactory.create_batch(3, is_cancelled=False)
        PaymentFactory.create_batch(3, is_cancelled=True)
        PaymentFactory.create_batch(2, is_paypal=True, is_cancelled=False)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_changelist_search_ok(self):
        response = self.client.get(self.url, {"q": "foo"})

        self.assertEqual(response.status_code, 200)


class ShippingCostsAdminSmokeTests(BaseAdminTestCase):
    url = reverse_lazy("admin:shop_shippingcost_changelist")

    def test_changelist_render(self):
        ShippingCostFactory.create()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_changelist_search_ok(self):
        response = self.client.get(self.url, {"q": "foo"})

        self.assertEqual(response.status_code, 200)
