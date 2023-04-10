import json

from django.urls import reverse

from django_webtest import WebTest

from ..constants import CART_SESSION_KEY
from .factories import PaymentMethodFactory


class CheckoutTests(WebTest):

    csrf_checks = False

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.payment_method = PaymentMethodFactory.create(
            name="Bank transfer", method="bank_transfer", enabled=True
        )

    def test_checkout_without_any_products(self):
        # ensure there is a cart in the session
        response = self.app.get(reverse("api:cart-detail"))
        assert response.status_code == 200
        cart_id = response.json["id"]
        assert self.app.session[CART_SESSION_KEY] == cart_id

        checkout_data = {
            "cart": cart_id,
            "payment_method": self.payment_method.id,
            "payment_method_options": None,
            "first_name": "Tony",
            "last_name": "Chocolonely",
            "email": "tony@example.com",
            "phone": "",
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
