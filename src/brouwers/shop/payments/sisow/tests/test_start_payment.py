from textwrap import dedent
from unittest.mock import patch

from django.test import RequestFactory, TestCase

import requests_mock

from ....models import ShopConfiguration
from ....tests.factories import PaymentFactory
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
