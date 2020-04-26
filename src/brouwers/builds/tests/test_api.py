from django.urls import reverse

from rest_framework.test import APITestCase

from brouwers.users.tests.factories import UserFactory

from .factories import BuildFactory


class SearchTests(APITestCase):

    def setUp(self):
        super().setUp()
        self.user1 = UserFactory.create(username='BBT')
        self.user2 = UserFactory.create(username='hanjos')

        self.builds_user1 = [
            BuildFactory.create(title='Sopwith Triplane', user=self.user1),
            BuildFactory.create(title='Honda McJugen', user=self.user1)
        ]
        self.builds_user2 = [
            BuildFactory.create(title='Monogram 4wheel drive', user=self.user2),
        ]
        self.url = reverse('api:builds:search')

    def test_search_user(self):
        """
        When searching by username, exact username matches must be returned
        and the builds by partial match.
        """
        response = self.client.get(self.url, data={'q': 'BBT'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, [
            {
                'display': 'BBT',
                'url': reverse('builds:user_build_list', kwargs={'user_id': self.user1.id}),
            },
            {
                'display': 'BBT - Honda McJugen',
                'url': reverse('builds:detail', kwargs={'slug': self.builds_user1[1].slug}),
            },
            {
                'display': 'BBT - Sopwith Triplane',
                'url': reverse('builds:detail', kwargs={'slug': self.builds_user1[0].slug}),
            },
        ])

    def test_search_title(self):
        """
        When searching a part of the title, builds must be returned that match.
        """
        response = self.client.get(self.url, data={'q': 'Tri'})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data, [
            {
                'display': 'BBT - Sopwith Triplane',
                'url': reverse('builds:detail', kwargs={'slug': self.builds_user1[0].slug}),
            },
        ])
