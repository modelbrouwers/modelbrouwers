import hashlib
from urllib.parse import urljoin

import lxml
import lxml.etree
import requests

from ...models import ShopConfiguration

BASE_URL = "https://www.sisow.nl/Sisow/iDeal/RestHandler.ashx/"
NS = "https://www.sisow.nl/Sisow/REST"


def xml_request(resource: str, method='get', **kwargs) -> lxml.etree.ElementTree:
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


def calculate_sha1(*args: str) -> str:
    sha1_input = "".join(args)
    sha1 = hashlib.sha1(sha1_input.encode('ascii'))
    digest = sha1.hexdigest()
    return digest


def calculate_ideal_sha1(purchaseid: str, merchantid: str, merchantkey: str, amount: int) -> str:
    return calculate_sha1(
        purchaseid,
        purchaseid,  # repeat purchase id for entrance code
        str(amount),
        "",  # empty shopid
        merchantid,
        merchantkey,
    )
