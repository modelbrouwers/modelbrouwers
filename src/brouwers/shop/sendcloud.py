"""
Implements a `Sendcloud`_ API client integration.

.. _Sendcloud: https://sendcloud.dev/
"""

from __future__ import annotations

import base64
import logging
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from io import BytesIO
from typing import Literal, NotRequired, TypedDict, assert_never
from urllib.parse import urljoin

from django.core.files import File

import requests
from requests.auth import HTTPBasicAuth

from .models import SendcloudShippingOption, ShopConfiguration

logger = logging.getLogger(__name__)

BASE_URL = "https://panel.sendcloud.sc/api/v3/"


class ShipWithProperties(TypedDict):
    shipping_option_code: str


class ShipWith(TypedDict):
    type: Literal["shipping_option_code"]
    properties: ShipWithProperties


type LegacyCountry = Literal["B", "D", "N"]
type CountryCode = Literal["BE", "DE", "NL"]


class ShippingAddress(TypedDict):
    name: str
    address_line_1: str
    postal_code: str
    city: str
    country_code: CountryCode
    company_name: NotRequired[str]
    house_number: NotRequired[str]


class SenderAddressID(TypedDict):
    sender_address_id: int


type WeightUnit = Literal["kg", "g"]


class Weight(TypedDict):
    value: str  # . as decimal separator
    unit: WeightUnit


class Parcel(TypedDict):
    weight: Weight


class ShipmentBody(TypedDict):
    ship_with: ShipWith
    to_address: ShippingAddress
    from_address: SenderAddressID
    parcels: list[Parcel]
    """
    1-15 items.
    """


class ShippingOptionsAddress(TypedDict):
    country_code: CountryCode


class ShippingOptionsBody(TypedDict):
    from_address: NotRequired[ShippingOptionsAddress]
    to_address: NotRequired[ShippingOptionsAddress]
    parcels: NotRequired[list[Parcel]]
    calculate_quotes: NotRequired[bool]


def _country_to_iso_country_code(country: LegacyCountry) -> CountryCode:
    match country:
        case "B":
            return "BE"
        case "D":
            return "DE"
        case "N":
            return "NL"
        case _:  # pragma: no cover
            assert_never(country)


class Client(requests.Session):
    """
    Interact with the sendcloud API.

    Testing guidelines: https://sendcloud.dev/docs/getting-started/creating-test-labels

    Flow from original v2 PHP client:

    1. Get available shipping methods.
        1. get suitable country, for each shipping method:
        2. Skip shipping method with ID 8
        3. Match the shipping method by checking countries ISO code against order
           shipping ISO code
        4. Repeat the above for each order to be shipped
    2. Create parcel for each order with name, company name, address, city, postal code,
       shipment ID, email, country, order number. requestShipment: false

    """

    _config: ShopConfiguration | None

    def __init__(self, config: ShopConfiguration | None = None):
        super().__init__()
        self._config = config
        self.headers["Accept"] = "application/json"

    @property
    def is_ready_for_use(self) -> bool:
        config = self.config
        if not config.sendcloud_public_key or not config.sendcloud_private_key:
            return False
        return True

    @property
    def config(self) -> ShopConfiguration:
        if self._config is None:
            self._config = ShopConfiguration.get_solo()
        return self._config

    def _configure_auth(self) -> None:
        if self.auth is None:
            config = self.config
            self.auth = HTTPBasicAuth(
                username=config.sendcloud_public_key,
                password=config.sendcloud_private_key,
            )

    def request(self, method: str | bytes, url: str | bytes, *args, **kwargs):
        assert isinstance(url, str)
        assert not url.startswith("/")
        self._configure_auth()
        abs_url = urljoin(BASE_URL, url)
        return super().request(method, abs_url, *args, **kwargs)

    def check_auth_ok(self) -> bool:
        response = self.get("user/auth/metadata")
        return response.ok

    def get_sender_address_id(self) -> int:
        response = self.get("addresses/sender-addresses")
        response.raise_for_status()
        sender_addresses = response.json()["data"]
        if len(sender_addresses) != 1:
            raise RuntimeError("Expected only a single sender address to be configured")
        return sender_addresses[0]["id"]

    def get_available_shipping_options(
        self, *, to_country: LegacyCountry
    ) -> Mapping[str, str]:
        country_code = _country_to_iso_country_code(to_country)
        body: ShippingOptionsBody = {
            "from_address": {"country_code": "NL"},
            "to_address": {"country_code": country_code},
        }
        response = self.post("shipping-options", json=body)
        response.raise_for_status()
        return {option["code"]: option["name"] for option in response.json()["data"]}

    def create_shipping_label(
        self,
        *,
        customer_name: str,
        street: str,
        number: str,
        postal_code: str,
        city: str,
        country: LegacyCountry,
        company: str = "",
        weight_in_grams: int,
    ) -> ShippingLabelResult:
        """
        Synchronously announce a shipment to create a shipping label.
        """
        country_code = _country_to_iso_country_code(country)
        if weight_in_grams > 1000:
            weight_unit = "kg"
            weight = str((Decimal(weight_in_grams) / 1000).quantize(Decimal("0.1")))
        else:
            weight_unit = "g"
            weight = str(weight_in_grams)

        shipping_option_code = SendcloudShippingOption.objects.get_code_for_country(
            country
        )

        body: ShipmentBody = {
            "ship_with": {
                "type": "shipping_option_code",
                "properties": {"shipping_option_code": shipping_option_code},
            },
            "to_address": {
                "name": customer_name,
                "address_line_1": f"{street} {number}",
                "postal_code": postal_code,
                "city": city,
                "country_code": country_code,
                "company_name": company,
                "house_number": number,
            },
            "from_address": {
                "sender_address_id": self.get_sender_address_id(),
            },
            "parcels": [
                {
                    "weight": {
                        "unit": weight_unit,
                        "value": weight,
                    },
                }
            ],
        }

        response = self.post("shipments/announce", json=body)
        response.raise_for_status()

        # The label is only returned if there's a single parcel in the shipment (!).
        data = response.json()["data"]
        assert len(data["parcels"]) == 1
        parcel_data = data["parcels"][0]

        match mime_type := data["label_details"]["mime_type"]:
            case "application/pdf":
                label_ext = ".pdf"
            case "image/png":
                label_ext = ".png"
            case "application/zpl":
                label_ext = ".zpl"
            case _:  # pragma: no cover
                raise NotImplementedError(f"Unexpected mime type {mime_type}")

        label_data = base64.b64decode(parcel_data["label_file"])
        return ShippingLabelResult(
            id=data["id"],
            label_file=File(BytesIO(label_data)),
            label_ext=label_ext,
            tracking_number=parcel_data["tracking_number"],
            tracking_url=parcel_data["tracking_url"],
        )

    def cancel_shipment(self, *, id: str) -> None:
        response = self.post(f"shipments/{id}/cancel")
        response.raise_for_status()
        data = response.json()["data"]
        logger.info("Cancel status: %s, message: %s", data["status"], data["message"])


@dataclass
class ShippingLabelResult:
    id: str
    label_file: File
    tracking_number: str
    tracking_url: str
    label_ext: str
