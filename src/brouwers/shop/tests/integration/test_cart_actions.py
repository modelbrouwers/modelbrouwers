from decimal import Decimal

from django.test import override_settings

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from brouwers.utils.tests.selenium import SeleniumTests

from ...models import Cart
from ..factories import CategoryFactory, ProductFactory


@override_settings(LANGUAGE_CODE="en")
class CartActionTests(SeleniumTests):
    def test_add_to_cart_from_detail_page(self):
        category = CategoryFactory.create(name="testdata")
        product = ProductFactory.create(
            name="integration test",
            price=Decimal("5.14"),
            vat=Decimal("0.20"),  # easier math in tests :-)
            categories=[category],
        )

        product_url = f"{self.live_server_url}{product.get_absolute_url()}"
        self.selenium.get(product_url)

        amount_input = self.selenium.find_element(By.NAME, "amount")
        amount_input.send_keys(Keys.DELETE, "3")

        add_button = self.selenium.find_element(
            By.CSS_SELECTOR, ".order-button .button.button--order"
        )
        add_button.click()

        WebDriverWait(self.selenium, timeout=3).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".cart__info"),
                "3 items",
            )
        )

        cart = Cart.objects.get()
        self.assertEqual(cart.products.count(), 1)
        cart_product = cart.products.get()
        self.assertEqual(cart_product.product, product)
        self.assertEqual(cart_product.amount, 3)
