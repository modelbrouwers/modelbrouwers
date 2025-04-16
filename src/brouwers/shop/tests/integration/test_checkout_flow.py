"""
Integration tests for shop checkout flow.
"""

from decimal import Decimal
from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from brouwers.general.constants import CountryChoices
from brouwers.utils.tests.selenium import SeleniumTests

from ...constants import OrderStatuses
from ...models import Cart, Order, ShopConfiguration
from ..factories import (
    CategoryFactory,
    PaymentMethodFactory,
    ProductFactory,
    ShippingCostFactory,
)


@override_settings(LANGUAGE_CODE="en")
class CheckoutTests(SeleniumTests):
    def test_checkout_cart_anonymous(self):
        """
        Checkout without using/creating a user account.

        1. The cart is populated with a number of products
        2. The checkout flow is entered and details filled out
        3. At the end, payment instructions must be displayed and an order reference
           visible.
        4. The order must contain all the entered data.
        """
        # 1. set up a basic catalogue and get a cart
        config = ShopConfiguration.get_solo()
        config.bank_transfer_instructions = "[bank transfer instructions here]"
        config.save()
        PaymentMethodFactory.create(
            name="Bank transfer", method="bank_transfer", enabled=True
        )
        category = CategoryFactory.create(name="testdata")
        ProductFactory.create(
            name="integration test",
            price=Decimal("5.14"),
            vat=Decimal("0.20"),  # easier math in tests :-)
            categories=[category],
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=100, price=Decimal("4.95")
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=1000, price=Decimal("9.95")
        )

        patcher = patch("brouwers.shop.api.views.get_ideal_banks", return_value=[])
        patcher.start()
        self.addCleanup(patcher.stop)

        with self.subTest("put products in cart"):
            # view category page (product list)
            category_url = f"{self.live_server_url}{category.get_absolute_url()}"
            self.selenium.get(category_url)

            # add product to cart
            add_button = self.selenium.find_element(
                By.CSS_SELECTOR, ".react-cart-actions .button.button__add"
            )
            add_button.click()

            WebDriverWait(self.selenium, timeout=3).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, ".cart__info"),
                    "1 item",
                )
            )

        # assert there's a cart before proceeding
        self.assertTrue(Cart.objects.exists())

        # 2. Enter checkout flow and fill out details
        with self.subTest("checkout: enter details"):

            checkout_url = f"{self.live_server_url}{reverse('shop:checkout')}"
            self.selenium.get(checkout_url)

            # continue without login/account creation
            link = self.selenium.find_element(
                By.PARTIAL_LINK_TEXT, "Continue without signup"
            )
            link.click()

            submit_button_locator = (By.CSS_SELECTOR, "form button.button--blue")
            submit_button = self.selenium.find_element(*submit_button_locator)
            self.assertEqual(submit_button.get_attribute("disabled"), "true")

            # fill out address details
            details = {
                "customer.firstName": "Tommy",
                "customer.lastName": "Tester",
                "customer.email": "tommy.tester@example.com",
                "deliveryAddress.street": "Voorstraat",
                "deliveryAddress.number": "18",
                "deliveryAddress.city": "Groot-Ammers",
                "deliveryAddress.postalCode": "2964AK",
            }

            for name, value in details.items():
                form_field = self.selenium.find_element(By.NAME, name)
                form_field.send_keys(value)

            WebDriverWait(self.selenium, timeout=3).until(
                EC.element_to_be_clickable(submit_button_locator)
            )
            submit_button.click()

        with self.subTest("checkout: payment"):
            self.assertTrue(self.selenium.current_url.endswith("/payment"))

            # select first payment method (bank transfer)
            self.selenium.find_element(By.CSS_SELECTOR, ".radio-option").click()

            # confirm & submit
            submit_button = self.selenium.find_element(
                By.CSS_SELECTOR, 'button[type="submit"]'
            )
            submit_button.click()

        with self.subTest("checkout: confirmation"):
            WebDriverWait(self.selenium, timeout=1).until(
                EC.url_matches(r".*/confirmation\?orderId=.*")
            )

            order = Order.objects.get()
            self.assertNotEqual(order.reference, "")

            panel_locator = (By.ID, "react-checkout")
            WebDriverWait(self.selenium, timeout=1).until(
                EC.text_to_be_present_in_element(panel_locator, order.reference)
            )
            panel = self.selenium.find_element(*panel_locator)
            self.assertIn("[bank transfer instructions here]", panel.text)

            # check order details
            with self.subTest("order details"):
                self.assertEqual(order.email, "tommy.tester@example.com")
                self.assertEqual(order.first_name, "Tommy")
                self.assertEqual(order.last_name, "Tester")
                self.assertEqual(order.status, OrderStatuses.received)

                # check address details
                self.assertIsNone(order.invoice_address)
                self.assertIsNotNone(order.delivery_address)
                self.assertEqual(order.delivery_address.street, "Voorstraat")
                self.assertEqual(order.delivery_address.number, "18")
                self.assertEqual(order.delivery_address.postal_code, "2964AK")
                self.assertEqual(order.delivery_address.city, "Groot-Ammers")
                self.assertEqual(order.delivery_address.country, "N")

                # check order cart contents
                self.assertIsNotNone(order.cart)
                cart_snapshot = order.cart.snapshot_data

                self.assertEqual(cart_snapshot["total"], "5.14")
                products = cart_snapshot["products"]
                self.assertEqual(len(products), 1)
                product = products[0]
                self.assertEqual(product["amount"], 1)
                self.assertEqual(product["name"], "integration test")
                self.assertEqual(product["price"], "5.14")
                self.assertEqual(product["total"], "5.14")
                self.assertEqual(product["vat"], "0.20")
