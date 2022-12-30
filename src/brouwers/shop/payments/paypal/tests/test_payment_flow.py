from typing import cast

from django.http.response import HttpResponseBase
from django.test import RequestFactory, TestCase
from django.urls import reverse

import requests_mock

from ....models import Payment
from ....tests.factories import PaymentMethodFactory
from ...service import start_payment
from .utils import patch_cache, patch_config

factory = RequestFactory()


class PaypalPaymentFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.pp = PaymentMethodFactory.create(name="paypal", method="paypal_standard")
        cls.bt = PaymentMethodFactory.create(
            name="bank transfer", method="bank_transfer"
        )

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
        payment = Payment.objects.create(
            payment_method=self.pp, amount=2542, reference="unit-test"
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
            f"http://testserver/winkel/payments/paypal/{payment.pk}/return?next=%2Ffoo",
        )
        self.assertEqual(
            experience_context["cancel_url"],
            f"http://testserver/winkel/payments/paypal/{payment.pk}/cancel"
            "?next=%2Fwinkel%2Fcheckout%2Fpayment",
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
        payment = Payment.objects.create(
            payment_method=self.pp,
            amount=2542,
            reference="unit-test",
            data={
                "paypal_order": {"id": "5O190127TN364715T"},
            },
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
