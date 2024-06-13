from decimal import Decimal

from django.test import SimpleTestCase, TestCase, override_settings

from brouwers.general.constants import CountryChoices

from ..models import ShippingCost
from .factories import ShippingCostFactory


class SimpleModelTests(SimpleTestCase):

    @override_settings(LANGUAGE_CODE="en")
    def test_repr(self):
        shipping_cost = ShippingCostFactory.build(
            label="small package",
            country="N",
            max_weight=275,
            price=Decimal("4.95"),
        )

        result = str(shipping_cost)

        self.assertEqual(result, "The Netherlands - small package, ≤ 275 g: € 4.95")

    @override_settings(LANGUAGE_CODE="nl")
    def test_format_weight(self):
        with self.subTest("grams"):
            shipping_cost_1 = ShippingCostFactory.build(max_weight=400)

            self.assertEqual(shipping_cost_1.format_weight(), "400 g")

        with self.subTest("kilograms"):
            shipping_cost_2 = ShippingCostFactory.build(max_weight=1560)

            self.assertEqual(shipping_cost_2.format_weight(), "1,56 kg")


class ModelTests(TestCase):

    def test_lookup_shipping_costs(self):
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=20, price=Decimal("2.95")
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=400, price=Decimal("9.95")
        )
        ShippingCostFactory.create(
            country=CountryChoices.be, max_weight=1000, price=Decimal("11.95")
        )

        price = ShippingCost.objects.get_price(country=CountryChoices.nl, weight=175)

        self.assertEqual(price, Decimal("9.95"))
