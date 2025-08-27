from decimal import Decimal

from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from brouwers.general.constants import CountryChoices
from brouwers.users.tests.factories import UserFactory

from ..constants import CART_SESSION_KEY, CartStatuses, WeightUnits
from ..models import Cart
from .factories import (
    CartFactory,
    CartProductFactory,
    ProductFactory,
    ShippingCostFactory,
)


class ProductApiTest(APITestCase):
    """
    Test that CRUD operations for products work correctly
    """

    def setUp(self):
        super().setUp()

        cache.clear()
        self.user = UserFactory.create()
        self.client.force_authenticate(user=self.user)
        self.addCleanup(cache.clear)

    def test_get_product(self):
        product = ProductFactory.create()

        response = self.client.get(reverse("api:product-detail", args=[product.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], product.pk)
        self.assertEqual(response.data["name"], product.name)


class CartApiTest(APITestCase):
    """
    Test that CRUD operations for cart work correctly
    """

    def setUp(self):
        super().setUp()

        cache.clear()
        self.user = UserFactory.create()
        self.client.force_authenticate(user=self.user)
        self.addCleanup(cache.clear)

    def test_get_cart(self):
        cart = CartFactory.create(user=self.user)

        response = self.client.get(reverse("api:cart-detail"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], cart.id)
        self.assertEqual(response.data["status"], cart.status)

        # Should return the last open cart
        open_cart = CartFactory.create(user=self.user, status=CartStatuses.open)
        closed_cart = CartFactory.create(user=self.user, status=CartStatuses.closed)

        response = self.client.get(reverse("api:cart-detail"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], open_cart.id)
        self.assertNotEqual(response.data["id"], closed_cart.id)

        # User shouldn't be able see other users' carts
        user2 = UserFactory.create()
        self.client.force_authenticate(user=user2)
        CartFactory.create(user=user2)

        response = self.client.get(reverse("api:cart-detail"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["id"], cart.id)

        # Anon user should get a new cart
        self.client.logout()

        response = self.client.get(reverse("api:cart-detail"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = response.data

        # Should get the same cart after the second request
        response2 = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["id"], cart["id"])

    def test_get_cart_product(self):
        cart = CartFactory.create(user=self.user)
        cart_product = CartProductFactory.create(cart=cart)

        response = self.client.get(
            reverse("api:cartproduct-detail", args=[cart_product.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], cart_product.pk)
        self.assertEqual(response.data["amount"], cart_product.amount)
        self.assertEqual(response.data["cart"], cart_product.cart.id)

        # User shouldn't be able see other users' cart products
        user2 = UserFactory.create()
        cart2 = CartFactory.create(user=user2)
        cart_product2 = CartProductFactory.create(cart=cart2)

        response = self.client.get(
            reverse("api:cartproduct-detail", args=[cart_product2.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_cart_products_by_cart(self):
        cart = CartFactory.create(user=self.user)
        CartProductFactory.create(cart=cart, amount=2)
        CartProductFactory.create(cart=cart, amount=20)

        response = self.client.get(reverse("api:cartproduct-list"), {"cart": cart.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_add_cart_product(self):
        cart = CartFactory.create(user=self.user)
        product = ProductFactory.create()
        data = {"product": product.id, "cart": cart.id, "amount": 13}

        response = self.client.post(reverse("api:cartproduct-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cart = Cart.objects.get(id=cart.id)
        self.assertEqual(cart.products.count(), 1)
        self.assertEqual(cart.products.first().amount, 13)

        # Update product amount
        cart_product = cart.products.first()
        data = {"amount": 2}
        self.client.patch(
            reverse("api:cartproduct-detail", args=[cart_product.pk]), data
        )
        cart = Cart.objects.get(id=cart.id)
        self.assertEqual(cart.products.count(), 1)
        self.assertEqual(cart.products.first().amount, 2)

        # Adding same product more than once should only update the amount
        cart = CartFactory.create(user=self.user)
        product = ProductFactory.create()
        data = {"product": product.id, "cart": cart.id, "amount": 1}

        self.client.post(reverse("api:cartproduct-list"), data)
        self.client.post(reverse("api:cartproduct-list"), data)

        cart = Cart.objects.get(id=cart.id)
        self.assertEqual(cart.products.count(), 1)

    def test_cart_products_total(self):
        product = ProductFactory.create(price=Decimal("1.15"))
        cart_product = CartProductFactory.create(
            product=product, amount=4, cart__user=self.user
        )

        response = self.client.get(
            reverse("api:cartproduct-detail", args=[cart_product.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], Decimal("4.60"))

    def test_get_cart_total(self):
        cart = CartFactory.create(user=self.user)
        product = ProductFactory.create(price=Decimal("1.15"))
        CartProductFactory.create(product=product, amount=4, cart=cart)
        product2 = ProductFactory.create(price=Decimal("0.15"))
        CartProductFactory.create(product=product2, amount=40, cart=cart)

        response = self.client.get(reverse("api:cart-detail"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total"], Decimal("10.60"))


class GetShippingCostsTests(APITestCase):
    def test_invalid_cart_id_parameter(self):
        endpoint = reverse("api:shipping-costs")
        cases = (
            ("missing cart_id", {}),
            ("cart_id empty", {"cart_id": ""}),
            ("cart_id not numeric", {"cart_id": "abc"}),
            (
                "cart_id points to closed cart",
                {"cart_id": CartFactory.create(status=CartStatuses.closed).pk},
            ),
            (
                "cart_id points to processing cart",
                {"cart_id": CartFactory.create(status=CartStatuses.processing).pk},
            ),
            (
                "cart_id does not exist",
                {"cart_id": Cart.objects.order_by("-pk")[:1][0].pk + 1},
            ),
        )
        for case, params in cases:
            with self.subTest(case=case):
                response = self.client.get(
                    endpoint, data={"country": CountryChoices.nl, **params}
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_country(self):
        cart = CartFactory.create(status=CartStatuses.open)
        session = self.client.session
        session[CART_SESSION_KEY] = cart.pk
        session.save()
        endpoint = reverse("api:shipping-costs")

        cases = (
            ("missing country param", {}),
            ("unsupported country param", {"country": "JA"}),
        )

        for case, params in cases:
            with self.subTest(case=case):
                response = self.client.get(
                    endpoint, data={"cart_id": cart.pk, **params}
                )

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_price_from_weight(self):
        endpoint = reverse("api:shipping-costs")
        cart = CartFactory.create(status=CartStatuses.open)
        session = self.client.session
        session[CART_SESSION_KEY] = cart.pk
        session.save()
        CartProductFactory.create(
            cart=cart,
            product__weight_unit=WeightUnits.gram,
            product__weight=150,
            amount=2,
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=100, price=Decimal("2.95")
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=400, price=Decimal("9.95")
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=1000, price=Decimal("19.95")
        )
        ShippingCostFactory.create(
            country=CountryChoices.be, max_weight=400, price=Decimal("11.95")
        )

        response = self.client.get(
            endpoint, data={"cart_id": cart.pk, "country": CountryChoices.nl}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], "9.95")
        self.assertEqual(response.data["weight"], "300 g")

    def test_calculate_cart_shipping_costs_more_than_1kg(self):
        endpoint = reverse("api:shipping-costs")
        cart = CartFactory.create(status=CartStatuses.open)
        session = self.client.session
        session[CART_SESSION_KEY] = cart.pk
        session.save()
        CartProductFactory.create(
            cart=cart,
            product__weight_unit=WeightUnits.gram,
            product__weight=550,
            amount=2,
        )
        ShippingCostFactory.create(
            country=CountryChoices.nl, max_weight=1000, price=Decimal("19.95")
        )

        response = self.client.get(
            endpoint,
            data={"cart_id": cart.pk, "country": CountryChoices.nl},
            HTTP_ACCEPT_LANGUAGE="nl",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["weight"], "1,1 kg")
        self.assertEqual(response.data["price"], "19.95")
