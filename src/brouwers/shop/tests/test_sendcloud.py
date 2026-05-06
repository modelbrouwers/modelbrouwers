import os
from decimal import Decimal

from brouwers.utils.tests.vcr import VCRTestCase

from ..models import ShopConfiguration
from ..sendcloud import Client
from .factories import SendcloudShippingOptionFactory


class SendcloudClientTests(VCRTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        config = ShopConfiguration.get_solo()
        config.sendcloud_public_key = os.getenv("SENDCLOUD_API_KEY", "")
        config.sendcloud_private_key = os.getenv("SENDCLOUD_API_SECRET", "")
        config.save()
        cls.addClassCleanup(config.clear_cache)

    def test_create_shipment_label(self):
        SendcloudShippingOptionFactory.create(country="N")

        with Client() as client:
            result = client.create_shipping_label(
                customer_name="Hanjos",
                street="Voorstraat",
                number="18",
                postal_code="2964AK",
                city="Groot-Ammers",
                country="N",
                weight_in_grams=Decimal(513),
            )

            # cancel the shipment to avoid potential costs!
            client.cancel_shipment(id=result.id)

        self.assertGreater(len(result.id), 0)
        self.assertGreater(len(result.label_file), 0)
        self.assertGreater(len(result.tracking_number), 0)
        self.assertGreater(len(result.tracking_url), 0)
