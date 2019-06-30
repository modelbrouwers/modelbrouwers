from django.test import SimpleTestCase, TestCase

from ...models import Payment, ShopConfiguration
from ..sisow.api import calculate_ideal_sha1
from ..sisow.forms import CallbackForm


class Sha1Tests(SimpleTestCase):

    def test_calculate_sha1(self):
        merchantid = "2537987391"
        merchantkey = "28f31a03f4d272bb5d6dd6a345cce93b670e2f79"
        purchaseid = "123"
        amount = "100"

        sha1 = calculate_ideal_sha1(
            purchaseid=purchaseid,
            merchantid=merchantid,
            merchantkey=merchantkey,
            amount=amount,
        )

        self.assertEqual(sha1, "4bdf789f7800496d9b5883eecd7eca2bae73cd02")


class CallbackFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        config = ShopConfiguration.get_solo()
        config.sisow_merchant_id = "2537987391"
        config.sisow_merchant_key = "28f31a03f4d272bb5d6dd6a345cce93b670e2f79"
        config.save()

        cls.payment = Payment(data={
            "sisow_transaction_request": {
                "trxid": "TEST080536811624",
            }
        })

    def test_valid_callback_form(self):
        form = CallbackForm(data={
            "trxid": "TEST080536811624",
            "ec": "4cb92ef9-0bcc-4a",
            "status": "Success",
            "sha1": "54f2ae81eaa39fd8463f0f780a228fc3562faa43",
        }, payment=self.payment)

        self.assertTrue(form.is_valid())

    def test_invalid_callback_form(self):
        form = CallbackForm(data={
            "trxid": "TEST080536811624",
            "ec": "4cb92ef9-0bcc-4a",
            "status": "Success",
            "sha1": "ad534db9faba53ac064e2140a87429334e855d98",  # bad hash
        }, payment=self.payment)

        self.assertFalse(form.is_valid())
