from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from brouwers.users.tests.factories import UserFactory

from ..constants import CartStatuses
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
        response = self.client.get(reverse('api:product-detail', args=[product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], product.pk)
        self.assertEqual(response.data['name'], product.name)
        self.assertEqual(response.data['brand'], product.brand.id)


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
        response = self.client.get(reverse('api:cart-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart']['id'], cart.id)
        self.assertEqual(response.data['cart']['status'], cart.status)

        # Should return the last open cart
        open_cart = CartFactory.create(user=self.user, status=CartStatuses.open)
        closed_cart = CartFactory.create(user=self.user, status=CartStatuses.paid)
        response = self.client.get(reverse('api:cart-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart']['id'], open_cart.id)
        self.assertNotEqual(response.data['cart']['id'], closed_cart.id)

        # User shouldn't be able see other users' carts
        user2 = UserFactory.create()
        self.client.force_authenticate(user=user2)
        cart2 = CartFactory.create(user=user2)
        response = self.client.get(reverse('api:cart-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data['cart']['id'], cart.id)

        # Anon user should get a new cart
        self.client.logout()
        response = self.client.get(reverse('api:cart-detail'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart = response.data['cart']

        # Should get the same cart after the second request
        response2 = self.client.get(reverse('api:cart-detail'))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['cart']['id'], cart['id'])

    def test_get_cart_product(self):
        cart = CartFactory.create(user=self.user)
        cart_product = CartProductFactory.create(cart=cart)
        response = self.client.get(reverse('api:cartproduct-detail', args=[cart_product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], cart_product.pk)
        self.assertEqual(response.data['amount'], cart_product.amount)
        self.assertEqual(response.data['cart'], cart_product.cart.id)

        # User shouldn't be able see other users' cart products
        user2 = UserFactory.create()
        cart2 = CartFactory.create(user=user2)
        cart_product2 = CartProductFactory.create(cart=cart2)
        response = self.client.get(reverse('api:cartproduct-detail', args=[cart_product2.pk]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
