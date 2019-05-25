from functools import lru_cache
from typing import Iterator, List
from urllib.parse import urljoin

from django.utils.translation import ugettext_lazy as _

import lxml
import lxml.etree
import requests
from djchoices import ChoiceItem, DjangoChoices

BASE_URL = "https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/"
NS = "https://www.sisow.nl/Sisow/REST"


def xml_request(resource: str, **params) -> lxml.etree.ElementTree:
    from ..models import ShopConfiguration

    config = ShopConfiguration.get_solo()

    if config.sisow_test_mode:
        params['test'] = 'true'

    url = urljoin(BASE_URL, resource)

    response = requests.get(url, params=params)
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
