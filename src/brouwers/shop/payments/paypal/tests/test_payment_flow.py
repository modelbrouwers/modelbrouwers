from typing import cast

from django.http.response import HttpResponseBase
from django.test import RequestFactory, TestCase
from django.urls import reverse

import requests_mock

from ....tests.factories import CartFactory, PaymentFactory, PaymentMethodFactory
from ...service import start_payment
from .utils import patch_cache, patch_config

factory = RequestFactory()


class PaypalPaymentFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        PaymentMethodFactory.create(name="paypal", method="paypal_standard")
        PaymentMethodFactory.create(name="bank transfer", method="bank_transfer")

    @patch_cache({"token": {"expires_in": 3600, "access_token": "brouwers-dummy"}})
    @requests_mock.Mocker()
    @patch_config()
    def test_happy_flow_start_payment(self, m, mock_get_solo):
        # From https://developer.paypal.com/docs/api/orders/v2/#orders-create-response
        m.post(
            "https://api-m.paypal.com/v2/checkout/orders",
            json={
                "id": "5O190127TN364715T",
                "status": "PAYER_ACTION_REQUIRED",
                "payment_source": {"paypal": {}},
                "links": [
                    {
                        "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
                        "rel": "self",
                        "method": "GET",
                    },
                    {
                        "href": "https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
                        "rel": "payer-action",
                        "method": "GET",
                    },
                ],
            },
        )
        # EUR 25.42
        payment = PaymentFactory.create(
            is_paypal=True,
            amount=2542,
            reference="unit-test",
            data={},
        )
        dummy_request = factory.post("/start-payment")

        result = start_payment(payment, dummy_request, next_page="/foo")

        self.assertIsNotNone(result)
        result = cast(HttpResponseBase, result)
        self.assertRedirects(
            result,
            "https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
            fetch_redirect_response=False,
        )
        payment.refresh_from_db()
        self.assertEqual(payment.data["paypal_order"]["id"], "5O190127TN364715T")

        create_data = m.last_request.json()
        self.assertEqual(create_data["intent"], "CAPTURE")
        self.assertEqual(
            create_data["purchase_units"],
            [
                {
                    "invoice_id": "unit-test",
                    "amount": {
                        "currency_code": "EUR",
                        "value": "25.42",
                    },
                }
            ],
        )
        experience_context = create_data["payment_source"]["paypal"][
            "experience_context"
        ]
        self.assertEqual(
            experience_context["return_url"],
            f"http://testserver/nieuwe-winkel/payments/paypal/{payment.pk}/return?next=%2Ffoo",
        )
        self.assertEqual(
            experience_context["cancel_url"],
            f"http://testserver/nieuwe-winkel/payments/paypal/{payment.pk}/cancel"
            "?next=%2Fnieuwe-winkel%2Fcheckout%2Fpayment",
        )

    @patch_cache({"token": {"expires_in": 3600, "access_token": "brouwers-dummy"}})
    @requests_mock.Mocker()
    @patch_config()
    def test_happy_flow_return_path(self, m, mock_get_solo):
        m.get(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
            json={
                "id": "5O190127TN364715T",
                "intent": "CAPTURE",
                "status": "APPROVED",
                "payment_source": {"paypal": {}},
                "links": [
                    {
                        "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
                        "rel": "self",
                        "method": "GET",
                    },
                    {
                        "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T/capture",
                        "rel": "capture",
                        "method": "POST",
                    },
                ],
            },
        )
        m.post(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T/capture",
            json={
                "id": "5O190127TN364715T",
                "intent": "CAPTURE",
                "status": "COMPLETED",
                "payment_source": {"paypal": {}},
                "links": [
                    {
                        "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
                        "rel": "self",
                        "method": "GET",
                    },
                ],
            },
        )
        payment = PaymentFactory.create(
            is_paypal=True,
            amount=2542,
            reference="unit-test",
            data={"paypal_order": {"id": "5O190127TN364715T"}},
        )
        return_url = reverse("shop:paypal-return", kwargs={"pk": payment.pk})
        confirmation_url = reverse("shop:checkout", kwargs={"path": "confirmation"})

        response = self.client.get(
            return_url,
            {
                "next": confirmation_url,
                "token": "5O190127TN364715T",
            },
        )

        self.assertRedirects(response, confirmation_url)
        capture = m.last_request
        self.assertEqual(capture.method, "POST")
        self.assertEqual(
            capture.url,
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T/capture",
        )
        self.assertIn("Paypal-Request-Id", capture.headers)

    def test_unhappy_flow_return_path(self):
        with self.subTest("accessing payment different payment method"):
            bt_payment = PaymentFactory.create(
                payment_method__method="bank_transfer", amount=1000
            )
            return_url = reverse("shop:paypal-return", kwargs={"pk": bt_payment.pk})

            response = self.client.get(return_url)

            self.assertEqual(response.status_code, 404)

        payment = PaymentFactory.create(
            is_paypal=True,
            amount=2542,
            data={"paypal_order": {"id": "5O190127TN364715T"}},
        )
        return_url = reverse("shop:paypal-return", kwargs={"pk": payment.pk})

        with self.subTest("missing token in URL"):
            response = self.client.get(return_url)

            self.assertEqual(response.status_code, 404)

        with self.subTest("different token in URL"):
            response = self.client.get(return_url, {"token": "different-value"})

            self.assertEqual(response.status_code, 404)

        with self.subTest("payment is missing metadata"):
            payment2 = PaymentFactory.create(is_paypal=True, amount=2542, data={})
            return_url2 = reverse("shop:paypal-return", kwargs={"pk": payment2.pk})

            response = self.client.get(return_url2)

            self.assertEqual(response.status_code, 404)

    @patch_cache({"token": {"expires_in": 3600, "access_token": "brouwers-dummy"}})
    @requests_mock.Mocker()
    @patch_config()
    def test_replay_of_return_url_payment_already_captured(self, m, mock_get_solo):
        payment = PaymentFactory.create(
            is_paypal=True,
            amount=2542,
            data={
                "paypal_order": {"id": "5O190127TN364715T"},
                "paypal_capture_request_id": "earlier-id",
            },
        )
        return_url = reverse("shop:paypal-return", kwargs={"pk": payment.pk})
        m.get(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
            json={
                "id": "5O190127TN364715T",
                "intent": "CAPTURE",
                "status": "COMPLETED",
                "payment_source": {"paypal": {}},
                "links": [
                    {
                        "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
                        "rel": "self",
                        "method": "GET",
                    },
                ],
            },
        )

        response = self.client.get(
            return_url,
            {
                "next": "/dummy",
                "token": "5O190127TN364715T",
            },
        )

        self.assertRedirects(response, "/dummy", fetch_redirect_response=False)
        self.assertEqual(len(m.request_history), 1)

    @patch_cache({"token": {"expires_in": 3600, "access_token": "brouwers-dummy"}})
    @requests_mock.Mocker()
    @patch_config()
    def test_validate_next_parameter(self, m, mock_get_solo):
        payment = PaymentFactory.create(
            is_paypal=True,
            amount=2542,
            data={"paypal_order": {"id": "5O190127TN364715T"}},
        )
        return_url = reverse("shop:paypal-return", kwargs={"pk": payment.pk})
        m.get(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
            json={
                "id": "5O190127TN364715T",
                "intent": "CAPTURE",
                "status": "COMPLETED",
                "payment_source": {"paypal": {}},
                "links": [
                    {
                        "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
                        "rel": "self",
                        "method": "GET",
                    },
                ],
            },
        )

        response = self.client.get(
            return_url,
            {
                "next": "https://evil.com/",
                "token": "5O190127TN364715T",
            },
        )

        self.assertRedirects(response, "/nieuwe-winkel/", fetch_redirect_response=False)

    def test_cancel_flow_error_conditions(self):
        with self.subTest("accessing payment different payment method"):
            bt_payment = PaymentFactory.create(
                payment_method__method="bank_transfer", amount=1000
            )
            cancel_url = reverse("shop:paypal-cancel", kwargs={"pk": bt_payment.pk})

            response = self.client.get(cancel_url)

            self.assertEqual(response.status_code, 404)

        payment = PaymentFactory.create(
            is_paypal=True,
            amount=2542,
            data={"paypal_order": {"id": "5O190127TN364715T"}},
        )
        cancel_url = reverse("shop:paypal-cancel", kwargs={"pk": payment.pk})

        with self.subTest("missing token in URL"):
            response = self.client.get(cancel_url)

            self.assertEqual(response.status_code, 404)

        with self.subTest("different token in URL"):
            response = self.client.get(cancel_url, {"token": "different-value"})

            self.assertEqual(response.status_code, 404)

        with self.subTest("payment is missing metadata"):
            payment2 = PaymentFactory.create(is_paypal=True, amount=2542, data={})
            cancel_url2 = reverse("shop:paypal-cancel", kwargs={"pk": payment2.pk})

            response = self.client.get(cancel_url2)

            self.assertEqual(response.status_code, 404)

    @patch_cache({"token": {"expires_in": 3600, "access_token": "brouwers-dummy"}})
    @requests_mock.Mocker()
    @patch_config()
    def test_cancel_flow_cart_still_in_session(self, m, mock_get_solo):
        cart = CartFactory.create()
        m.get(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
            json={
                "id": "5O190127TN364715T",
                "status": "PAYER_ACTION_REQUIRED",
                "payment_source": {"paypal": {}},
                "links": [
                    {
                        "href": "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
                        "rel": "self",
                        "method": "GET",
                    },
                    {
                        "href": "https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
                        "rel": "payer-action",
                        "method": "GET",
                    },
                ],
            },
        )
        payment = PaymentFactory.create(
            is_paypal=True,
            order__cart=cart,
            amount=2542,
            data={"paypal_order": {"id": "5O190127TN364715T"}},
        )
        cancel_url = reverse("shop:paypal-cancel", kwargs={"pk": payment.pk})
        checkout_url = reverse("shop:checkout", kwargs={"path": "payment"})

        response = self.client.get(
            cancel_url,
            {
                "token": "5O190127TN364715T",
                "next": checkout_url,
            },
        )

        self.assertRedirects(response, checkout_url)
        # check that the detail status was fetched in API
        self.assertEqual(
            m.last_request.url,
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
        )
        self.assertEqual(m.last_request.method, "GET")

        api_response = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(api_response.status_code, 200)
        cart_data = api_response.json()
        self.assertEqual(cart_data["id"], cart.id)
        self.assertEqual(cart_data["status"], "open")
