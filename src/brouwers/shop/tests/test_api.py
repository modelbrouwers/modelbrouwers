from django.core.cache import cache
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from brouwers.users.tests.factories import UserFactory
from .factories import ProductFactory


class CartApiTest(APITransactionTestCase):
    """
      Test that CRUD operations for a cart work correctly
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
