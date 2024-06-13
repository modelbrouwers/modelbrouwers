from decimal import Decimal

from django.test import SimpleTestCase, TestCase, override_settings

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
