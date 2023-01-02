from io import StringIO

from django.core.management import call_command
from django.test import TestCase

import requests_mock

from ....tests.factories import PaymentFactory
from .utils import patch_cache, patch_config


def patch_paypal_config(func):
    patched_cache = patch_cache(
        {"token": {"expires_in": 3600, "access_token": "brouwers-dummy"}}
    )
    return patched_cache(patch_config()(func))


def _build_detail_json(order_id: str, status: str):
    links = [
        {
            "href": f"https://api-m.paypal.com/v2/checkout/orders/{order_id}",
            "rel": "self",
            "method": "GET",
        }
    ]
    if status == "APPROVED":
        links.append(
            {
                "href": f"https://api-m.paypal.com/v2/checkout/orders/{order_id}/capture",
                "rel": "capture",
                "method": "POST",
            }
        )
    return {
        "id": order_id,
        "intent": "CAPTURE",
        "status": status,
        "payment_source": {"paypal": {}},
        "links": links,
    }


@requests_mock.Mocker()
class ClaimPaymentsCommandTests(TestCase):
    @patch_paypal_config
    def test_claim_approved(self, m, *mocks):
        m.get(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
            json=_build_detail_json("5O190127TN364715T", "APPROVED"),
        )
        m.get(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364826R",
            json=_build_detail_json("5O190127TN364826R", "COMPLETED"),
        )
        m.get(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364937Q",
            json=_build_detail_json("5O190127TN364937Q", "PAYER_ACTION_REQUIRED"),
        )
        m.post(
            "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T/capture",
            json=_build_detail_json("5O190127TN364715T", "COMPLETED"),
        )
        payment = PaymentFactory.create(
            is_paypal=True,
            amount=2542,
            reference="test",
            data={"paypal_order": {"id": "5O190127TN364715T"}},
        )
        payment_done = PaymentFactory.create(
            is_paypal=True,
            amount=1000,
            reference="test-completed",
            data={
                "paypal_order": {
                    "id": "5O190127TN364826R",
                    "status": "COMPLETED",
                }
            },
        )
        payment_pending = PaymentFactory.create(
            is_paypal=True,
            amount=1000,
            reference="test-pending",
            data={"paypal_order": {"id": "5O190127TN364937Q"}},
        )
        stdout, stderr = StringIO(), StringIO()

        call_command("claim_paypal_payments", stdout=stdout, stderr=stderr)

        self.assertEqual(stderr.getvalue(), "")
        output = stdout.getvalue().strip()
        self.assertEqual(output, f"Captured payments: {payment.pk}.")
        self.assertNotIn(str(payment_done.pk), output)
        self.assertNotIn(str(payment_pending.pk), output)

        self.assertEqual(len(m.request_history), 3)
        capture_requests = [
            req
            for req in m.request_history
            if req.url.endswith("/capture") and req.method == "POST"
        ]
        self.assertEqual(len(capture_requests), 1)
        detail_requests = [req for req in m.request_history if req.method == "GET"]
        self.assertEqual(len(detail_requests), 2)
        detail_urls = {req.url for req in detail_requests}
        self.assertEqual(
            detail_urls,
            {
                "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364715T",
                "https://api-m.paypal.com/v2/checkout/orders/5O190127TN364937Q",
            },
        )
