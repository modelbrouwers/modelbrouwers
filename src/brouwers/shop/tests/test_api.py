from decimal import Decimal

from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from brouwers.users.tests.factories import UserFactory

from ..constants import CartStatuses
from ..models import Cart
from .factories import CartFactory, CartProductFactory, ProductFactory


class ProductApiTest(APITransactionTestCase):
    """
    Test that CRUD operations for products work correctly
    """

    def setUp(self):
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
        self.assertEqual(response.data["brand"], product.brand.id)


class CartApiTest(APITransactionTestCase):
    """
    Test that CRUD operations for cart work correctly
    """

    def setUp(self):
        cache.clear()
        self.user = UserFactory.create()
        self.client.force_authenticate(user=self.user)
        self.addCleanup(cache.clear)

    def test_get_cart(self):
        cart = CartFactory.create(user=self.user)
        response = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cart"]["id"], cart.id)
        self.assertEqual(response.data["cart"]["status"], cart.status)

        # Should return the last open cart
        open_cart = CartFactory.create(user=self.user, status=CartStatuses.open)
        closed_cart = CartFactory.create(user=self.user, status=CartStatuses.paid)
        response = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cart"]["id"], open_cart.id)
        self.assertNotEqual(response.data["cart"]["id"], closed_cart.id)

        # User shouldn't be able see other users' carts
        user2 = UserFactory.create()
        self.client.force_authenticate(user=user2)
        cart2 = CartFactory.create(user=user2)
        response = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["cart"]["id"], cart.id)

        # Anon user should get a new cart
        self.client.logout()
        response = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = response.data["cart"]

        # Should get the same cart after the second request
        response2 = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["cart"]["id"], cart["id"])

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
        cart_product = CartProductFactory.create(product=product, amount=4, cart=cart)
        product2 = ProductFactory.create(price=Decimal("0.15"))
        cart_product2 = CartProductFactory.create(
            product=product2, amount=40, cart=cart
        )
        response = self.client.get(reverse("api:cart-detail"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cart"]["total"], Decimal("10.60"))
