from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory
from .factories import BuildFactory


class SearchTests(APITestCase):

    def setUp(self):
        super(SearchTests, self).setUp()
        self.user1 = UserFactory.create(username='BBT')
        self.user2 = UserFactory.create(username='hanjos')

        self.builds_user1 = [
            BuildFactory.create(title='Sopwith Triplane'),
            BuildFactory.create(title='Honda McJugen')
        ]
        self.builds_user2 = [
            BuildFactory.create(title='Monogram 4wheel drive'),
        ]
        self.url = reverse('api:builds:search')

    def test_search_user(self):
        """
        When searching by username, exact username matches must be returned
        and the builds by partial match.
        """
        raise NotImplementedError
