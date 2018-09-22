from django.test import TestCase

from ..backends import EmailModelBackend
from .factories import UserFactory


class LoginBackendTests(TestCase):

    def setUp(self):
        super(LoginBackendTests, self).setUp()
        self.user = UserFactory.create(email='test@test.com', password='secret')

    def test_email_backend(self):
        backend = EmailModelBackend()
        user = backend.authenticate(username='test@test.com', password='secret')
        self.assertEqual(user, self.user)

        # wrong password / email
        self.assertIsNone(backend.authenticate(username='test@test.com', password='guesswhat'))
        self.assertIsNone(backend.authenticate(username='imakenosense', password='secret'))
