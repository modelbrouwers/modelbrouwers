import csv
import io
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ..constants import WeightUnits
from ..models import Category
from .factories import CartFactory, CartProductFactory, CategoryFactory, ProductFactory


class CategoryImportExportTest(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.superuser = UserFactory.create(is_staff=True, is_superuser=True)

    def test_export(self):
        CategoryFactory.create()
        url = reverse("admin:shop_category_export")
        categories = self.app.get(url, user=self.superuser)
        form = categories.forms[1]
        form["format"].select("0")
        response = form.submit()

        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        headers = body.pop(0)
        export_fields = ["id", "name", "image", "enabled", "meta_description"]

        self.assertEqual(headers, export_fields)


class CategoryModelTest(TestCase):
    def test_nesting(self):
        root = Category.add_root(name="Root")
        self.assertEqual(root.name, "Root")

        child1 = root.add_child(name="Child")
        child1.save()
        child2 = root.add_child(name="Child2")
        child2.save()

        self.assertEqual(len(root.get_children()), 2)

        child1.add_child()
        self.assertEqual(len(child1.get_children()), 1)


class ProductModelTests(TestCase):
    def test_calculate_weight_in_grams(self):
        with self.subTest("gram units"):
            product1 = ProductFactory.create(weight_unit=WeightUnits.gram, weight=300)

            self.assertEqual(product1.weight_in_grams, 300)
        with self.subTest("kg units"):
            product2 = ProductFactory.create(
                weight_unit=WeightUnits.kilogram, weight=Decimal("0.55")
            )

            self.assertEqual(product2.weight_in_grams, 550)


class CartModelTests(TestCase):
    def test_calculate_total(self):
        cart = CartFactory.create()
        CartProductFactory.create(
            cart=cart,
            product__price=Decimal(10),
            amount=2,
        )
        CartProductFactory.create(
            cart=cart,
            product__price=Decimal(5),
            amount=1,
        )

        total = cart.total

        self.assertEqual(total, Decimal(25))

    def test_calculate_weight(self):
        cart = CartFactory.create()
        CartProductFactory.create(
            cart=cart,
            product__weight_unit=WeightUnits.kilogram,
            product__weight=Decimal(0.6),
            amount=2,
        )
        CartProductFactory.create(
            cart=cart,
            product__weight_unit=WeightUnits.gram,
            product__weight=Decimal(150),
            amount=1,
        )

        weight = cart.weight

        self.assertEqual(weight, 1350)
