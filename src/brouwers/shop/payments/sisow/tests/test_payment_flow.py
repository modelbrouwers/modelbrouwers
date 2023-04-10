from textwrap import dedent
from typing import cast
from unittest.mock import patch

from django.test import RequestFactory, TestCase
from django.urls import reverse

import requests_mock

from ....constants import CartStatuses, PaymentStatuses
from ....models import ShopConfiguration
from ....tests.factories import PaymentFactory
from ..api import calculate_sha1
from ..constants import TransactionStatuses
from ..exceptions import InvalidIssuerURL
from ..service import start_payment

factory = RequestFactory()


# Credentials from example requests in Documentation PDF rest521.pdf
@patch(
    "brouwers.shop.payments.sisow.service.ShopConfiguration.get_solo",
    return_value=ShopConfiguration(
        sisow_merchant_id="2537987391",
        sisow_merchant_key="28f31a03f4d272bb5d6dd6a345cce93b670e2f79",
    ),
)
class PaymentStartTests(TestCase):
    @requests_mock.Mocker()
    def test_happy_flow_mistercash(self, m_get_solo, m):
        dummy_request = factory.post("/start-payment")
        payment = PaymentFactory.create(
            is_mistercash=True,
            reference="order-134",
            amount=67,
            data={"sisow_method": "mistercash"},
        )

        m.post(
            "https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/TransactionRequest",
            text=dedent(
                """
                <?xml version="1.0" encoding="UTF-8"?>
                <transactionrequest xmlns="https://www.sisow.nl/Sisow/REST" version="1.0.0">
                    <transaction>
                        <issuerurl>https%3a%2f%2fideal.bunq.com%2f%3fauthorisationId%3d647366083227%26transactionId%3d0050002676740002</issuerurl>
                        <trxid>0050002676740002</trxid>
                    </transaction>
                    <signature>
                        <sha1>4b693b5202629b60c715010916aaee255bedddde</sha1>
                    </signature>
                </transactionrequest>
            """
            ).strip(),
        )

        redirect_url = start_payment(payment, dummy_request, next_page="/foo")

        self.assertEqual(
            redirect_url,
            "https://ideal.bunq.com/?authorisationId=647366083227&transactionId=0050002676740002",
        )

    @requests_mock.Mocker()
    def test_with_invalid_signature(self, m_get_solo, m):
        dummy_request = factory.post("/start-payment")
        payment = PaymentFactory.create(
            is_mistercash=True,
            reference="order-134",
            amount=67,
            data={"sisow_method": "mistercash"},
        )

        m.post(
            "https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/TransactionRequest",
            text=dedent(
                """
                <?xml version="1.0" encoding="UTF-8"?>
                <transactionrequest xmlns="https://www.sisow.nl/Sisow/REST" version="1.0.0">
                    <transaction>
                        <issuerurl>https://evil.com/payme</issuerurl>
                        <trxid>0050002676740002</trxid>
                    </transaction>
                    <signature>
                        <sha1>4b693b5202629b60c715010916aaee255bedddde</sha1>
                    </signature>
                </transactionrequest>
            """
            ).strip(),
        )

        with self.assertRaises(InvalidIssuerURL):
            start_payment(payment, dummy_request, next_page="/foo")


# Credentials from example requests in Documentation PDF rest521.pdf
@patch(
    "brouwers.shop.payments.sisow.forms.ShopConfiguration.get_solo",
    return_value=ShopConfiguration(
        sisow_merchant_id="2537987391",
        sisow_merchant_key="28f31a03f4d272bb5d6dd6a345cce93b670e2f79",
    ),
)
class PaymentReturnFlowTests(TestCase):
    def test_return_with_missing_ec(self, m_get_solo):
        payment = PaymentFactory.create(
            is_mistercash=True,
            reference="order-134",
            amount=67,
        )
        url = reverse("shop:sisow-payment-callback", kwargs={"pk": payment.pk})

        response = self.client.get(
            url,
            {
                "trxid": payment.data["sisow_transaction_request"]["trxid"],
                "ec": "",
                "status": cast(str, TransactionStatuses.success),
                "sha1": "definitely-bad-hash",
                "notify": False,
                "callback": False,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_return_url_with_invalid_hash(self, m_get_solo):
        payment = PaymentFactory.create(
            is_mistercash=True,
            reference="order-134",
            amount=67,
        )
        url = reverse("shop:sisow-payment-callback", kwargs={"pk": payment.pk})

        response = self.client.get(
            url,
            {
                "trxid": payment.data["sisow_transaction_request"]["trxid"],
                "ec": "order-134",
                "status": cast(str, TransactionStatuses.success),
                "sha1": "definitely-bad-hash",
                "notify": False,
                "callback": False,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_notify_callback_no_redirect(self, m_get_solo):
        payment = PaymentFactory.create(
            is_mistercash=True, reference="order-134", amount=67
        )
        trxid = payment.data["sisow_transaction_request"]["trxid"]
        url = reverse("shop:sisow-payment-callback", kwargs={"pk": payment.pk})

        response = self.client.get(
            url,
            {
                "trxid": trxid,
                "ec": "order-134",
                "status": cast(str, TransactionStatuses.success),
                "sha1": calculate_sha1(
                    trxid,
                    "order-134",
                    "Success",
                    "2537987391",
                    "28f31a03f4d272bb5d6dd6a345cce93b670e2f79",
                ),
                "notify": True,
                "callback": False,
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_payment_cancelled(self, m_get_solo):
        payment = PaymentFactory.create(
            is_mistercash=True, reference="order-134", amount=67
        )
        trxid = payment.data["sisow_transaction_request"]["trxid"]
        url = reverse("shop:sisow-payment-callback", kwargs={"pk": payment.pk})

        response = self.client.get(
            url,
            {
                "trxid": trxid,
                "ec": "order-134",
                "status": cast(str, TransactionStatuses.failure),
                "sha1": calculate_sha1(
                    trxid,
                    "order-134",
                    "Failure",
                    "2537987391",
                    "28f31a03f4d272bb5d6dd6a345cce93b670e2f79",
                ),
            },
        )

        self.assertEqual(response.status_code, 302)
        payment.refresh_from_db()

        self.assertEqual(payment.data["status"], "Failure")
        self.assertEqual(payment.status, PaymentStatuses.cancelled)
        self.assertIsNotNone(payment.historical_order)
        self.assertIsNone(payment.order)

        cart = payment.historical_order.cart
        # compare against cart retrieved via frontend api call
        response = self.client.get(reverse("api:cart-detail"))
        assert response.status_code == 200
        cart_id = response.json()["id"]
        self.assertEqual(cart.id, cart_id)
        self.assertEqual(cart.status, CartStatuses.open)

    def test_payment_success(self, m_get_solo):
        payment = PaymentFactory.create(
            is_mistercash=True, reference="order-134", amount=67
        )
        trxid = payment.data["sisow_transaction_request"]["trxid"]
        url = reverse("shop:sisow-payment-callback", kwargs={"pk": payment.pk})

        response = self.client.get(
            url,
            {
                "trxid": trxid,
                "ec": "order-134",
                "status": cast(str, TransactionStatuses.success),
                "sha1": calculate_sha1(
                    trxid,
                    "order-134",
                    "Success",
                    "2537987391",
                    "28f31a03f4d272bb5d6dd6a345cce93b670e2f79",
                ),
            },
        )

        self.assertEqual(response.status_code, 302)
        payment.refresh_from_db()

        self.assertEqual(payment.data["status"], "Success")
        self.assertEqual(payment.status, PaymentStatuses.completed)
        self.assertIsNone(payment.historical_order)
        self.assertIsNotNone(payment.order)

        cart = payment.order.cart
        # compare against cart retrieved via frontend api call
        response = self.client.get(reverse("api:cart-detail"))
        assert response.status_code == 200
        cart_id = response.json()["id"]
        self.assertNotEqual(cart.id, cart_id)
        self.assertEqual(cart.status, CartStatuses.open)
