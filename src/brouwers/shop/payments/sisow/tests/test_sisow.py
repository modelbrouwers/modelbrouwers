from django.test import SimpleTestCase, TestCase

import requests_mock

from ....models import Payment, ShopConfiguration
from ...sisow.api import calculate_sisow_sha1
from ...sisow.forms import CallbackForm
from ...sisow.service import get_ideal_bank_choices


class Sha1Tests(SimpleTestCase):
    def test_calculate_sha1(self):
        merchantid = "2537987391"
        merchantkey = "28f31a03f4d272bb5d6dd6a345cce93b670e2f79"
        purchaseid = "123"
        amount = "100"

        sha1 = calculate_sisow_sha1(
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

        cls.payment = Payment(
            reference="4cb92ef9-0bcc-4a",
            data={
                "sisow_transaction_request": {
                    "trxid": "TEST080536811624",
                }
            },
        )

    def test_valid_callback_form(self):
        form = CallbackForm(
            data={
                "trxid": "TEST080536811624",
                "ec": "4cb92ef9-0bcc-4a",
                "status": "Success",
                "sha1": "54f2ae81eaa39fd8463f0f780a228fc3562faa43",
            },
            payment=self.payment,
        )

        self.assertTrue(form.is_valid())

    def test_invalid_callback_form(self):
        form = CallbackForm(
            data={
                "trxid": "TEST080536811624",
                "ec": "4cb92ef9-0bcc-4a",
                "status": "Success",
                "sha1": "ad534db9faba53ac064e2140a87429334e855d98",  # bad hash
            },
            payment=self.payment,
        )

        self.assertFalse(form.is_valid())


class ServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        config = ShopConfiguration.get_solo()
        config.sisow_merchant_id = "2537987391"
        config.sisow_merchant_key = "28f31a03f4d272bb5d6dd6a345cce93b670e2f79"
        config.save()

    def test_get_ideal_bank_choices(self):
        with requests_mock.mock() as m:
            m.get(
                "https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/DirectoryRequest",
                text="""<?xml version="1.0" encoding="UTF-8"?>
<directoryresponse xmlns="https://www.sisow.nl/Sisow/REST" version="1.0.0">
<directory>
    <issuer>
        <issuerid>01</issuerid>
        <issuername>ABN Amro Bank</issuername>
    </issuer>
    <issuer>
        <issuerid>02</issuerid>
        <issuername>ASN Bank</issuername>
    </issuer>
    <issuer>
        <issuerid>05</issuerid>
        <issuername>ING</issuername>
    </issuer>
    <issuer>
        <issuerid>06</issuerid>
        <issuername>Rabobank</issuername>
    </issuer>
    <issuer>
        <issuerid>07</issuerid>
        <issuername>SNS Bank</issuername>
    </issuer>
    <issuer>
        <issuerid>08</issuerid>
        <issuername>RegioBank</issuername>
    </issuer>
    <issuer>
        <issuerid>09</issuerid>
        <issuername>Triodos Bank</issuername>
    </issuer>
    <issuer>
        <issuerid>10</issuerid>
        <issuername>Van Lanschot Bankiers</issuername>
    </issuer>
    <issuer>
        <issuerid>11</issuerid>
        <issuername>Knab</issuername>
    </issuer>
    <issuer>
        <issuerid>12</issuerid>
        <issuername>bunq</issuername>
    </issuer>
</directory>
</directoryresponse>""",
            )

            choices = list(get_ideal_bank_choices())

        self.assertEqual(
            choices,
            [
                ("01", "ABN Amro Bank"),
                ("02", "ASN Bank"),
                ("05", "ING"),
                ("06", "Rabobank"),
                ("07", "SNS Bank"),
                ("08", "RegioBank"),
                ("09", "Triodos Bank"),
                ("10", "Van Lanschot Bankiers"),
                ("11", "Knab"),
                ("12", "bunq"),
            ],
        )
