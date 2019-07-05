from functools import lru_cache
from typing import Iterator, List
from urllib.parse import unquote

from django.urls import reverse

from ...models import Payment, ShopConfiguration
from .api import NS, calculate_ideal_sha1, calculate_sha1, xml_request
from .constants import Payments
from .exceptions import InvalidIssuerURL


class iDealBank:

    def __init__(self, _id: str, name: str):
        self.id = _id
        self.name = name


@lru_cache()
def get_ideal_banks() -> List[iDealBank]:
    root = xml_request('DirectoryRequest')
    _issuers = root.findall("*/{{{ns}}}issuer".format(ns=NS))
    banks = [
        iDealBank(
            _id=issuer.find("{{{ns}}}issuerid".format(ns=NS)).text,
            name=issuer.find("{{{ns}}}issuername".format(ns=NS)).text,
        )
        for issuer in _issuers
    ]
    return banks


def get_ideal_bank_choices() -> Iterator:
    for bank in get_ideal_banks():
        yield (bank.id, bank.name)


def start_ideal_payment(payment: Payment, request=None) -> str:
    bank_id = payment.data.get("bank")
    if not isinstance(bank_id, int):
        raise ValueError("Missing selected bank ID in payment data")

    config = ShopConfiguration.get_solo()

    purchaseid = payment.reference

    sha1 = calculate_ideal_sha1(
        purchaseid,
        config.sisow_merchant_id,
        config.sisow_merchant_key,
        str(payment.amount),
    )

    callback_url = reverse('shop:sisow-payment-callback', kwargs={"pk": payment.pk})
    if request:
        callback_url = request.build_absolute_uri(callback_url)

    post_data = {
        "merchantid": config.sisow_merchant_id,
        "payment": Payments.ideal,
        "purchaseid": purchaseid,
        "amount": payment.amount,
        "description": "Example description",
        "returnurl": callback_url,
        "sha1": sha1,
        "issuerid": bank_id,
        "currency": "EUR",
    }

    root = xml_request('TransactionRequest', method="post", data=post_data)

    # verify the response
    transaction = root.find("{{{ns}}}transaction".format(ns=NS))

    url = transaction.find("{{{ns}}}issuerurl".format(ns=NS)).text
    trx_id = transaction.find("{{{ns}}}trxid".format(ns=NS)).text
    signature_sha1 = root.find("{{{ns}}}signature/{{{ns}}}sha1".format(ns=NS)).text
    expected_sha1 = calculate_sha1(trx_id, url, config.sisow_merchant_id, config.sisow_merchant_key)
    if signature_sha1 != expected_sha1:
        raise InvalidIssuerURL("Mismatch in issuer URL sha1")

    # store metadata in payment object
    payment.data["sisow_transaction_request"] = {
        "issuerurl": url,
        "trxid": trx_id,
        "signature_sha1": signature_sha1,
    }
    payment.save()

    return unquote(url)
