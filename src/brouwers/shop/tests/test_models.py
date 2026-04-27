import csv
import io
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ..constants import OrderStatuses, PaymentStatuses, WeightUnits
from ..models import Category, Order
from .factories import (
    CartFactory,
    CartProductFactory,
    CategoryFactory,
    OrderFactory,
    ProductFactory,
)


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
        export_fields = [
            "id",
            "name",
            "image",
            "enabled",
            "meta_description",
            "path",
            "depth",
            "numchild",
        ]

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

        child1.add_child(name="nested child")
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


class OrderModelTests(TestCase):
    def test_detect_changed_fields(self):
        with self.subTest("identical instances"):
            order = OrderFactory.build()

            changed_fields = Order.get_changed_fields(order, order)

            self.assertEqual(len(changed_fields), 0)

        with self.subTest("changed status and t&t codes"):
            order1 = OrderFactory.build(
                status=OrderStatuses.processing,
                track_and_trace_code="code1",
                track_and_trace_link="https://t.and.trace/link1",
            )
            order2 = OrderFactory.build(
                status=OrderStatuses.cancelled,
                track_and_trace_code="code2",
                track_and_trace_link="https://t.and.trace/link2",
            )

            changed_fields = Order.get_changed_fields(order1, order2)

            self.assertEqual(len(changed_fields), 3)
            self.assertEqual(
                set(changed_fields),
                {"status", "track_and_trace_code", "track_and_trace_link"},
            )

        with self.subTest("payment status changes are detected"):
            order3 = OrderFactory.create(
                with_payment=True, payment__status=PaymentStatuses.pending
            )
            order4 = Order.objects.select_related("payment").get(pk=order3.pk)
            order4.payment.status = PaymentStatuses.cancelled
            order4.payment.save()

            changed_fields = Order.get_changed_fields(order3, order4)

            self.assertEqual(len(changed_fields), 1)
            self.assertEqual(changed_fields[0], "payment.status")

    def test_actionable_orders_without_payment(self):
        combinations = [
            (OrderStatuses.received, True),
            (OrderStatuses.processing, False),
            (OrderStatuses.shipped, False),
            (OrderStatuses.cancelled, False),
        ]
        _all_statuses = [c[0] for c in combinations]
        for value in OrderStatuses.values:
            assert value in _all_statuses

        for status, expected in combinations:
            with self.subTest(status=status):
                order = OrderFactory.create(with_payment=False, status=status)

                self.assertEqual(order.is_actionable, expected)

    def test_actionable_orders_with_payment(self):
        combinations = [
            (OrderStatuses.received, PaymentStatuses.pending, False),
            (
                OrderStatuses.received,
                PaymentStatuses.completed,
                True,
            ),
            (OrderStatuses.received, PaymentStatuses.cancelled, False),
            (OrderStatuses.processing, PaymentStatuses.pending, False),
            (OrderStatuses.processing, PaymentStatuses.completed, False),
            (OrderStatuses.processing, PaymentStatuses.cancelled, False),
            (OrderStatuses.shipped, PaymentStatuses.pending, False),
            (OrderStatuses.shipped, PaymentStatuses.completed, False),
            (OrderStatuses.shipped, PaymentStatuses.cancelled, False),
            (OrderStatuses.cancelled, PaymentStatuses.pending, False),
            (OrderStatuses.cancelled, PaymentStatuses.completed, False),
            (OrderStatuses.cancelled, PaymentStatuses.cancelled, False),
        ]

        for status, payment_status, expected in combinations:
            with self.subTest(status=status):
                order = OrderFactory.create(
                    with_payment=True, status=status, payment__status=payment_status
                )

                self.assertEqual(order.is_actionable, expected)
