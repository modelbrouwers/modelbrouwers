import json
from decimal import Decimal
from unittest.mock import patch

from django.core import mail
from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest

from brouwers.general.constants import CountryChoices
from brouwers.utils.tests.html_assert import strip_all_attributes

from ..constants import CART_SESSION_KEY, CartStatuses, DeliveryMethods
from ..models import Cart, Order, ShopConfiguration
from .factories import (
    CartProductFactory,
    CategoryFactory,
    PaymentMethodFactory,
    ProductFactory,
    ShippingCostFactory,
)


class CheckoutTests(WebTest):
    csrf_checks = False

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.payment_method = PaymentMethodFactory.create(
            name="Bank transfer", method="bank_transfer", enabled=True
        )

        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=100, price=Decimal("4.95")
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=1000, price=Decimal("9.95")
        )

    def _get_cart_id(self) -> int:
        # ensure there is a cart in the session
        response = self.app.get(reverse("api:cart-detail"))
        assert response.status_code == 200
        cart_id = response.json["id"]
        assert self.app.session[CART_SESSION_KEY] == cart_id
        return cart_id

    def test_checkout_without_any_products(self):
        cart_id = self._get_cart_id()
        checkout_data = {
            "cart": cart_id,
            "payment_method": self.payment_method.id,
            "payment_method_options": None,
            "first_name": "Tony",
            "last_name": "Chocolonely",
            "email": "tony@example.com",
            "phone": "",
            "delivery_method": DeliveryMethods.mail,
            "delivery_address": {
                "street": "Sesamstraat",
                "number": "101",
                "postal_code": "1111AA",
                "city": "Abcoude",
                "country": "N",
                "company": "",
                "chamber_of_commerce": "",
            },
        }

        url = reverse("shop:confirm-checkout")

        response = self.app.post(url, {"checkoutData": json.dumps(checkout_data)})

        self.assertEqual(
            response.status_code, 200
        )  # validation errors emitted in the body
        errors = json.loads(response.pyquery("#checkout-errors").text())
        self.assertIn("cart", errors)

    def test_checkout_with_products_and_delivery_via_email(self):
        # set up mocks
        mock_config = ShopConfiguration(
            bank_transfer_instructions="[bank transfer instructions here]",
            from_email="shop@example.com",
        )
        patch_paths = (
            "brouwers.shop.payments.payment_options",
            "brouwers.shop.emails",
        )
        for path in patch_paths:
            patcher = patch(
                f"{path}.ShopConfiguration.get_solo", return_value=mock_config
            )
            patcher.start()
            self.addCleanup(patcher.stop)
        # set up test data
        category = CategoryFactory.create(name="testdata")
        product1 = ProductFactory.create(
            name="Testproduct",
            price=Decimal("5.14"),
            vat=Decimal("0.20"),  # easier math in tests :-)
            categories=[category],
            weight=100,  # grams
        )
        product2 = ProductFactory.create(
            name="Testproduct",
            price=Decimal("10.00"),
            vat=Decimal("0.20"),  # easier math in tests :-)
            categories=[category],
            weight=30,  # grams
        )
        cart_id = self._get_cart_id()
        cart = Cart.objects.get(pk=cart_id)
        CartProductFactory.create(cart=cart, product=product1, amount=3)
        CartProductFactory.create(cart=cart, product=product2, amount=2)
        assert cart.weight == 360
        checkout_data = {
            "cart": cart_id,
            "payment_method": self.payment_method.id,
            "payment_method_options": None,
            "first_name": "Tony",
            "last_name": "Chocolonely",
            "email": "tony@example.com",
            "phone": "",
            "delivery_method": DeliveryMethods.mail,
            "delivery_address": {
                "street": "Sesamstraat",
                "number": "101",
                "postal_code": "1111AA",
                "city": "Abcoude",
                "country": "N",
                "company": "",
                "chamber_of_commerce": "",
            },
        }

        # fetch expected/calculated shipping costs displayed in frontend to ensure
        # both places calculate the same value
        shipping_costs_response = self.app.get(
            reverse("api:shipping-costs"),
            params={
                "cart_id": cart_id,
                "country": checkout_data["delivery_address"]["country"],
            },
        )
        assert shipping_costs_response.status_code == 200
        expected_shipping_costs = Decimal(shipping_costs_response.json["price"])

        url = reverse("shop:confirm-checkout")

        with self.captureOnCommitCallbacks(execute=True):
            response = self.app.post(
                url,
                {"checkoutData": json.dumps(checkout_data)},
                extra_environ={"HTTP_ACCEPT_LANGUAGE": "nl"},
            )

        self.assertEqual(response.status_code, 302)

        order = Order.objects.get()

        with self.subTest("shipping costs endpoint sanity check"):
            self.assertEqual(order.shipping_costs, expected_shipping_costs)

        with self.subTest("email sent"):
            self.assertEqual(len(mail.outbox), 1)
            message = mail.outbox[0]
            self.assertEqual(message.from_email, "shop@example.com")

            self.assertIn(order.reference, str(message.subject))
            self.assertEqual(message.extra_headers, {"Content-Language": "nl"})

            content_by_content_type = {
                ct: content for content, ct in message.alternatives
            }
            self.assertIn("text/html", content_by_content_type)

            html_body = strip_all_attributes(content_by_content_type["text/html"])

            # check that the correct prices are in the HTML e-mail
            with self.subTest("first product"):
                self.assertInHTML("<td>&euro;&nbsp;5,14</td>", html_body)
                self.assertInHTML("<td>&euro;&nbsp;15,42</td>", html_body)

            with self.subTest("second product"):
                self.assertInHTML("<td>&euro;&nbsp;10,00</td>", html_body)
                self.assertInHTML("<td>&euro;&nbsp;20,00</td>", html_body)

            with self.subTest("shipping costs"):
                self.assertIn(_("Shipping costs"), html_body)
                self.assertInHTML("<td>&euro;&nbsp;9,95</td>", html_body)

            with self.subTest("totals"):
                # 0.20 * 3 * 5.14 + 0.20 * 2 * 10 -> rounded = 7.08
                # 35.42 + 9.95 = 45.37 (products + shipping)
                self.assertInHTML("<td>&euro;&nbsp;7,08</td>", html_body)
                self.assertInHTML("<td>&euro;&nbsp;45,37</td>", html_body)

    def test_checkout_delivery_by_mail_without_delivery_address_is_blocked(self):
        self.addCleanup(ShopConfiguration.clear_cache)
        # set up test data
        cart_id = self._get_cart_id()
        cart = Cart.objects.get(pk=cart_id)
        CartProductFactory.create(cart=cart)
        checkout_data = {
            "cart": cart_id,
            "payment_method": self.payment_method.id,
            "payment_method_options": None,
            "first_name": "Tony",
            "last_name": "Chocolonely",
            "email": "tony@example.com",
            "phone": "",
            "delivery_address": None,
            "delivery_method": DeliveryMethods.mail,
        }
        url = reverse("shop:confirm-checkout")

        response = self.app.post(url, {"checkoutData": json.dumps(checkout_data)})

        self.assertEqual(response.status_code, 200)
        errors = response.context["serializer"].errors
        self.assertIn("delivery_address", errors)

    def test_checkout_pickup_in_shop(self):
        self.addCleanup(ShopConfiguration.clear_cache)
        # set up test data
        cart_id = self._get_cart_id()
        cart = Cart.objects.get(pk=cart_id)
        CartProductFactory.create(cart=cart)
        checkout_data = {
            "cart": cart_id,
            "payment_method": self.payment_method.id,
            "payment_method_options": None,
            "first_name": "Tony",
            "last_name": "Chocolonely",
            "email": "tony@example.com",
            "phone": "",
            "delivery_address": None,
            "delivery_method": DeliveryMethods.pickup,
        }
        url = reverse("shop:confirm-checkout")

        response = self.app.post(url, {"checkoutData": json.dumps(checkout_data)})

        self.assertEqual(response.status_code, 302)
        cart.refresh_from_db()
        self.assertEqual(cart.status, CartStatuses.processing)
        order = Order.objects.get()
        self.assertEqual(order.cart, cart)
        self.assertEqual(order.shipping_costs, 0)
        self.assertIsNone(order.delivery_address)
        self.assertIsNone(order.invoice_address)
