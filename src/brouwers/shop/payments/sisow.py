import hashlib
import uuid
from decimal import Decimal
from functools import lru_cache
from typing import Iterator, List
from urllib.parse import unquote, urljoin

from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

import lxml
import lxml.etree
import requests
from djchoices import ChoiceItem, DjangoChoices

BASE_URL = "https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/"
NS = "https://www.sisow.nl/Sisow/REST"


class InvalidIssuerURL(Exception):
    pass


def xml_request(resource: str, method='get', **kwargs) -> lxml.etree.ElementTree:
    from ..models import ShopConfiguration

    config = ShopConfiguration.get_solo()

    if config.sisow_test_mode:
        kwargs.setdefault('params', {})
        kwargs['params']['test'] = 'true'
        if 'data' in kwargs:
            kwargs['data'].setdefault('testmode', "true")

    url = urljoin(BASE_URL, resource)

    response = requests.request(method, url, **kwargs)
    response.raise_for_status()

    root = lxml.etree.fromstring(response.content)
    return root


class Payments(DjangoChoices):
    """
    Possible payment methods
    """
    ideal = ChoiceItem("ideal", label=_("iDEAL"))
    idealqr = ChoiceItem("idealqr", label=_("iDEAL QR"))
    overboeking = ChoiceItem("overboeking", label=_("Bankoverboeking"))
    ebill = ChoiceItem("ebill", label=_("Ebill"))
    bunq = ChoiceItem("bunq", label=_("bunq"))
    creditcard = ChoiceItem("creditcard", label=_("Creditcard"))
    maestro = ChoiceItem("maestro", label=_("Maestro"))
    vpay = ChoiceItem("vpay", label=_("V PAY"))
    sofort = ChoiceItem("sofort", label=_("SOFORT Banking"))
    giropay = ChoiceItem("giropay", label=_("Giropay"))
    eps = ChoiceItem("eps", label=_("EPS"))
    mistercash = ChoiceItem("mistercash", label=_("Bancontact"))
    belfius = ChoiceItem("belfius", label=_("Belfius Pay Button"))
    homepay = ChoiceItem("homepay", label=_("ING Home’Pay"))
    kbc = ChoiceItem("kbc", label=_("KBC"))
    cbc = ChoiceItem("cbc", label=_("CBC"))
    paypalec = ChoiceItem("paypalec", label=_("PayPal Express Checkout"))
    afterpay = ChoiceItem("afterpay", label=_("Afterpay"))
    billink = ChoiceItem("billink", label=_("Billink achteraf betalen"))
    capayable = ChoiceItem("capayable", label=_("Capayable gespreid betalen"))
    focum = ChoiceItem("focum", label=_("Focum AchterafBetalen"))
    klarna = ChoiceItem("klarna", label=_("Klarna Factuur"))
    vvv = ChoiceItem("vvv", label=_("VVV Giftcard"))
    webshop = ChoiceItem("webshop", label=_("Webshop Giftcard"))


class TransactionStatuses(DjangoChoices):
    success = ChoiceItem("Success", label=_("Een succesvolle transactie"))
    expired = ChoiceItem("Expired", label=_("De transactie is verlopen"))
    cancelled = ChoiceItem("Cancelled", label=_("De transactie is geannuleerd"))
    failure = ChoiceItem("Failure", label=_("Een interne fout heeft zich bij de gekozen betaalmethode voorgedaan"))
    pending = ChoiceItem("Pending", label=_("In afwachting van daadwerkelijke betaling, betaling is nog niet zeker"))
    reversed = ChoiceItem("Reversed", label=_("De transactie is teruggedraaid"))
    denied = ChoiceItem("Denied", label=_("De transactie aanvraag is afgewezen door de betaalmethode (Focum/Klarna)"))
    reservation = ChoiceItem(
        "Reservation",
        label=_("Transactie aanvraag is gelukt factuur dient nog te worden aangemaakt (Focum/Klarna)")
    )
    open = ChoiceItem("Open", label=_("De transactie is nog in behandeling"))


class CallbackForm(forms.Form):
    trxid = forms.CharField(label=_("transaction id"))
    ec = forms.CharField(label=_("entrance code"), required=False)
    status = forms.ChoiceField(label=_("status"), choices=TransactionStatuses.choices)
    sha1 = forms.CharField(label=_("sha1 transaction"))
    notify = forms.BooleanField(label=_("notify or not?"), required=False)
    callback = forms.BooleanField(label=_("callback or not?"), required=False)

    def clean(self):
        from ..models import ShopConfiguration
        config = ShopConfiguration.get_solo()

        sha1 = self.cleaned_data.get("sha1")
        trxid = self.cleaned_data.get("trxid")
        ec = self.cleaned_data.get("ec")
        status = self.cleaned_data.get("status")

        if all((sha1, trxid, ec, status)):
            sha1_input = "{trxid}{ec}{status}{merchantid}{merchantkey}".format(
                trxid=trxid,
                ec=ec,
                status=status,
                merchantid=config.sisow_merchant_id,
                merchantkey=config.sisow_merchant_key,
            )
            check_sha1 = hashlib.sha1(sha1_input.encode('ascii'))
            digest = check_sha1.hexdigest()
            print(digest)
            if not digest == sha1:
                self.add_error("sha1", _("Invalid SHA1"))


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


def coerce_bank(value):
    bank_mapping = {bank.id: bank for bank in get_ideal_banks()}
    return bank_mapping[value]


def calculate_sha1(purchaseid: str, merchantid: str, merchantkey: str, amount: str, shopid: str = "") -> str:
    sha1_input = "{purchaseid}{entrancecode}{amount}{shopid}{merchantid}{merchantkey}".format(
        purchaseid=purchaseid,
        entrancecode=purchaseid,
        amount=amount,
        merchantid=merchantid,
        merchantkey=merchantkey,
        shopid=shopid
    )

    sha1 = hashlib.sha1(sha1_input.encode('ascii'))
    digest = sha1.hexdigest()
    return digest


def start_ideal_payment(amount: Decimal, bank: iDealBank, request=None) -> str:
    from ..models import ShopConfiguration

    config = ShopConfiguration.get_solo()

    purchaseid = str(uuid.uuid4())[:16]
    amount = int(100 * amount)  # convert euros to eurocents

    sha1 = calculate_sha1(
        purchaseid=purchaseid,
        merchantid=config.sisow_merchant_id,
        merchantkey=config.sisow_merchant_key,
        amount=amount
    )

    callback_url = reverse('shop:payment-callback')
    if request:
        callback_url = request.build_absolute_uri(callback_url)

    post_data = {
        "merchantid": config.sisow_merchant_id,
        "payment": Payments.ideal,
        "purchaseid": purchaseid,
        "amount": amount,
        "description": "Example description",
        "returnurl": callback_url,
        "sha1": sha1,
        "issuerid": bank.id,
        "currency": "EUR",
    }

    root = xml_request('TransactionRequest', method="post", data=post_data)

    # verify the response
    transaction = root.find("{{{ns}}}transaction".format(ns=NS))

    url = transaction.find("{{{ns}}}issuerurl".format(ns=NS)).text
    trx_id = transaction.find("{{{ns}}}trxid".format(ns=NS)).text
    signature_sha1 = root.find("{{{ns}}}signature/{{{ns}}}sha1".format(ns=NS)).text

    validation_string = f"{trx_id}{url}{config.sisow_merchant_id}{config.sisow_merchant_key}"

    expected_sha1 = hashlib.sha1(validation_string.encode('ascii')).hexdigest()
    if signature_sha1 != expected_sha1:
        raise InvalidIssuerURL("Mismatch in issuer URL sha1")

    return unquote(url)
