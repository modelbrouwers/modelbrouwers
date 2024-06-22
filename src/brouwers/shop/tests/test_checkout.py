import json
from decimal import Decimal
from unittest.mock import patch

from django.core import mail
from django.urls import reverse

from django_webtest import WebTest

from brouwers.utils.tests.html_assert import strip_all_attributes

from ..constants import CART_SESSION_KEY, DeliveryMethods
from ..models import Cart, Order, ShopConfiguration
from .factories import (
    CartProductFactory,
    CategoryFactory,
    PaymentMethodFactory,
    ProductFactory,
)


class CheckoutTests(WebTest):

    csrf_checks = False

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.payment_method = PaymentMethodFactory.create(
            name="Bank transfer", method="bank_transfer", enabled=True
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

    def test_checkout_sends_confirmation_email(self):
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
        )
        product2 = ProductFactory.create(
            name="Testproduct",
            price=Decimal("10.00"),
            vat=Decimal("0.20"),  # easier math in tests :-)
            categories=[category],
        )
        cart_id = self._get_cart_id()
        cart = Cart.objects.get(pk=cart_id)
        CartProductFactory.create(cart=cart, product=product1, amount=3)
        CartProductFactory.create(cart=cart, product=product2, amount=2)
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

        with self.captureOnCommitCallbacks(execute=True):
            response = self.app.post(
                url,
                {"checkoutData": json.dumps(checkout_data)},
                extra_environ={"HTTP_ACCEPT_LANGUAGE": "nl"},
            )

        self.assertEqual(response.status_code, 302)

        with self.subTest("email sent"):
            self.assertEqual(len(mail.outbox), 1)
            message = mail.outbox[0]
            self.assertEqual(message.from_email, "shop@example.com")

            order = Order.objects.get()
            self.assertIn(order.reference, message.subject)
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

            with self.subTest("totals"):
                # 0.20 * 3 * 5.14 + 0.20 * 2 * 10 -> rounded = 7.08
                self.assertInHTML("<td>&euro;&nbsp;7,08</td>", html_body)
                self.assertInHTML("<td>&euro;&nbsp;35,42</td>", html_body)
