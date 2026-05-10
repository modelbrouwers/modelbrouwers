import os

from django.conf import settings
from django.urls import reverse

from brouwers.general.constants import CountryChoices
from brouwers.shop.models import ShopConfiguration
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.vcr import VCRTestCase

from ...constants import DeliveryMethods, WeightUnits
from ...sendcloud import Client
from ..factories import CartProductFactory, OrderFactory, SendcloudShippingOptionFactory


class OrderShippingLabelAccessTests(VCRTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        SendcloudShippingOptionFactory.create(
            country=CountryChoices.nl, shipping_option_code="sendcloud:letter"
        )

        cls.order = OrderFactory.create(
            delivery_method=DeliveryMethods.mail,
            delivery_address__street="Voorstraat",
            delivery_address__number="18",
            delivery_address__postal_code="2964AK",
            delivery_address__city="Groot-Ammers",
            delivery_address__country=CountryChoices.nl,
        )
        CartProductFactory.create(
            cart=cls.order.cart,
            product__weight=200,
            product__weight_unit=WeightUnits.gram,
        )
        cls.detail_url = reverse(
            "shop:order-shipping-label", kwargs={"reference": cls.order.reference}
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
                assert not self.order.shipping_label

                response = self.client.post(self.detail_url)

                self.assertEqual(response.status_code, 403)

    def test_sufficient_permissions(self):
        config = ShopConfiguration.get_solo()
        config.sendcloud_public_key = os.getenv("SENDCLOUD_API_KEY", "dummy-for-ci")
        config.sendcloud_private_key = os.getenv("SENDCLOUD_API_SECRET", "dummy-for-ci")
        config.save()
        self.addCleanup(config.clear_cache)
        user = UserFactory.create(permissions=["shop.change_order"])
        self.client.force_login(user)

        with (
            self.subTest("create label"),
            Client(config) as client,
        ):
            create_response = self.client.post(self.detail_url)

            self.assertEqual(create_response.status_code, 302)
            self.order.refresh_from_db()
            client.cancel_shipment(id=self.order.sendcloud_shipment_id)

        with self.subTest("download label"):
            download_response = self.client.get(self.detail_url)

            self.assertEqual(download_response.status_code, 200)


class FunctionalOrderShippingLabelTests(VCRTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        config = ShopConfiguration.get_solo()
        config.sendcloud_public_key = os.getenv("SENDCLOUD_API_KEY", "dummy-for-ci")
        config.sendcloud_private_key = os.getenv("SENDCLOUD_API_SECRET", "dummy-for-ci")
        config.save()
        cls.addClassCleanup(config.clear_cache)
        SendcloudShippingOptionFactory.create(
            country=CountryChoices.nl, shipping_option_code="sendcloud:letter"
        )

        cls.user = UserFactory.create(superuser=True)

    def setUp(self):
        super().setUp()

        self.client.force_login(self.user)

    def test_only_allows_orders_that_require_shipping(self):
        order = OrderFactory.create(delivery_method=DeliveryMethods.pickup)
        detail_url = reverse(
            "shop:order-shipping-label", kwargs={"reference": order.reference}
        )

        with self.subTest("create label"):
            create_response = self.client.post(detail_url)

            self.assertEqual(create_response.status_code, 404)

        with self.subTest("download label"):
            create_response = self.client.get(detail_url)

            self.assertEqual(create_response.status_code, 404)

    def test_can_create_label_only_if_none_exists_yet(self):
        order = OrderFactory.create(
            delivery_method=DeliveryMethods.mail,
            delivery_address__street="Voorstraat",
            delivery_address__number="18",
            delivery_address__postal_code="2964AK",
            delivery_address__city="Groot-Ammers",
            delivery_address__country=CountryChoices.nl,
        )
        assert not order.shipping_label
        CartProductFactory.create(
            cart=order.cart,
            product__weight=200,
            product__weight_unit=WeightUnits.gram,
        )
        detail_url = reverse(
            "shop:order-shipping-label", kwargs={"reference": order.reference}
        )

        with (
            self.subTest("label creation ok"),
            Client() as client,
        ):
            create_response = self.client.post(detail_url)

            self.assertRedirects(
                create_response,
                reverse("shop:order-detail", kwargs={"reference": order.reference}),
            )
            order.refresh_from_db()
            client.cancel_shipment(id=order.sendcloud_shipment_id)
            self.assertNotEqual(order.shipping_label, "")
            self.assertTrue(
                order.shipping_label.storage.exists(order.shipping_label.name)
            )

        with self.subTest("additional label creation attempts are blocked"):
            create_response = self.client.post(detail_url)

            self.assertEqual(create_response.status_code, 403)
