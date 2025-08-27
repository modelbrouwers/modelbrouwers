from collections.abc import Iterator
from dataclasses import dataclass
from functools import lru_cache
from typing import cast
from urllib.parse import unquote

from django.http import HttpRequest
from django.urls import reverse
from django.utils import translation

from furl import furl

from ...models import Payment, ShopConfiguration
from .api import NS, calculate_sha1, calculate_sisow_sha1, xml_request
from .constants import SisowMethods
from .exceptions import InvalidIssuerURL


@dataclass
class iDealBank:
    id: str
    name: str


@lru_cache
def get_ideal_banks() -> list[iDealBank]:
    root = xml_request("DirectoryRequest")
    _issuers = root.findall(f"*/{{{NS}}}issuer")
    banks = [
        iDealBank(
            id=issuer.find(f"{{{NS}}}issuerid").text,
            name=issuer.find(f"{{{NS}}}issuername").text,
        )
        for issuer in _issuers
    ]
    return banks


def get_ideal_bank_choices() -> Iterator[tuple[str, str]]:
    for bank in get_ideal_banks():
        yield (bank.id, bank.name)


def start_payment(payment: Payment, request: HttpRequest, next_page="") -> str:
    method: str = payment.data["sisow_method"]

    # ideal accepts an optional issuer ID for bank pre-selection
    extra_params = {}
    if method == SisowMethods.ideal:
        bank_id = payment.data.get("bank")
        if isinstance(bank_id, int):
            extra_params["issuerid"] = (bank_id,)

    config = cast(ShopConfiguration, ShopConfiguration.get_solo())

    purchaseid = payment.reference

    sha1 = calculate_sisow_sha1(
        purchaseid,
        config.sisow_merchant_id,
        config.sisow_merchant_key,
        payment.amount,
    )

    callback_url = reverse("shop:sisow-payment-callback", kwargs={"pk": payment.pk})
    callback_url = request.build_absolute_uri(callback_url)

    if next_page:
        callback_url = furl(callback_url).set({"next": next_page}).url

    post_data = {
        "merchantid": config.sisow_merchant_id,
        "payment": method,
        "purchaseid": purchaseid,
        "amount": payment.amount,
        "description": f"MB order {payment.reference}",  # TODO: parametrize?
        "returnurl": callback_url,
        "notifyurl": callback_url,
        # "notifyurl": "", TODO: server-to-server call
        "sha1": sha1,
        "currency": "EUR",
        "locale": translation.get_language(),
        **extra_params,
    }

    root = xml_request("TransactionRequest", method="post", data=post_data)

    # verify the response
    transaction = root.find(f"{{{NS}}}transaction")

    url = transaction.find(f"{{{NS}}}issuerurl").text
    trx_id = transaction.find(f"{{{NS}}}trxid").text
    signature_sha1 = root.find(f"{{{NS}}}signature/{{{NS}}}sha1").text
    # this pattern is the general case - applies for ideal, mrcash and sofort
    expected_sha1 = calculate_sha1(
        trx_id, url, config.sisow_merchant_id, config.sisow_merchant_key
    )
    if signature_sha1 != expected_sha1:
        raise InvalidIssuerURL("Mismatch in issuer URL sha1")

    # store metadata in payment object
    # TODO: ensure this is always stored whether the django transaction fails or succeeds
    payment.data["sisow_transaction_request"] = {
        "issuerurl": url,
        "trxid": trx_id,
        "signature_sha1": signature_sha1,
    }
    payment.save()

    return unquote(url)
