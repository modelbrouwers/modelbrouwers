from django.test import TestCase
from django.core import mail

from brouwers.general.models import PasswordReset
from .factory_models import UserFactory


class ResetTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_can_submit_reset(self):
        """ Test that a user can succesfully create a password reset """
        url = '/reset_pw/'

        self.assertEqual(PasswordReset.objects.count(), 0)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 0)

        # try username request
        data = {
            'forum_nickname': self.user.username,
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/login/')

        # verify that an e-mail was sent
        self.assertEqual(len(mail.outbox), 1)

        # verify that the password reset is indeed created
        self.assertEqual(PasswordReset.objects.count(), 1)

        # test e-mail
        response = self.client.post(url, {'email': self.user.email})
        self.assertRedirects(response, '/login/')

        # one extra e-mail in the outbox
        self.assertEqual(len(mail.outbox), 2)

        # verify that the password reset is indeed created
        self.assertEqual(PasswordReset.objects.count(), 2)
