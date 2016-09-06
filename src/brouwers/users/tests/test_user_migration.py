from django.contrib.auth import SESSION_KEY
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.http import int_to_base36

from brouwers.forum_tools.tests.factory_models import ForumUserFactory

from ..mail import UserCreatedFromForumEmail
from ..tokens import activation_token_generator
from .factories import UserFactory


class ActivationEmailTests(TestCase):
    def setUp(self):
        self.forum_user = ForumUserFactory()
        self.user = UserFactory(forumuser_id=self.forum_user.user_id, is_active=False)
        self.mail = UserCreatedFromForumEmail(**{'user': self.user})

    def test_content(self):
        """ Test that the expected context is present in the body of the e-mail. """
        token = activation_token_generator.make_token(self.user)
        uidb36 = int_to_base36(self.user.id)
        url = reverse('users:activate', kwargs={'token': token, 'uidb36': uidb36})

        text_content = self.mail.get_text_content()
        self.assertIsNotNone(text_content)

        self.assertIn(self.user.username, text_content)
        self.assertIn(token, text_content)
        self.assertIn(url, text_content)

        html_content = self.mail.get_html_content()
        self.assertIsNotNone(html_content)

        self.assertIn(self.user.username, html_content)
        self.assertIn(token, html_content)
        self.assertIn(url, html_content)

    def test_email_receivers(self):
        self.assertEqual(len(mail.outbox), 0)
        self.mail.send()
        self.assertEqual(len(mail.outbox), 1)

        m = mail.outbox.pop(0)

        self.assertIn(self.user.email, m.recipients())
        self.assertEqual(len(m.recipients()), 1)


class UserActivationFlowTestCase(TestCase):
    """
    Test the entire flow:
        * ForumUser tries signing in -> create user
          & send e-mail TODO
        * Get link from e-mail, request page
        * Test that the user is logged in
        * Test that the user is redirected to the profile
    """

    def setUp(self):
        self.forum_user = ForumUserFactory()

    def test_activation_view(self):
        """
        Test that the user is activated and redirected with a correct token
        """
        user = UserFactory(forumuser_id=self.forum_user.pk, is_active=False)
        token = activation_token_generator.make_token(user)
        uidb36 = int_to_base36(user.id)

        url = reverse('users:activate', kwargs={'token': token, 'uidb36': uidb36})
        self.assertIsNotNone(url)

        response = self.client.get(url)
        dest = reverse('users:profile')

        # check that the user is logged in
        user_id = self.client.session.get(SESSION_KEY)
        self.assertEqual(user.id, int(user_id))

        self.assertRedirects(response, dest)

    def test_wrong_token(self):
        """
        Test that a 403 forbidden is raised with an incorrect token.
        """
        user = UserFactory(forumuser_id=self.forum_user.pk, is_active=False)
        user2 = UserFactory(forumuser_id=self.forum_user.pk, is_active=False)

        token = activation_token_generator.make_token(user2)
        uidb36 = int_to_base36(user.id)

        url = reverse('users:activate', kwargs={'token': token, 'uidb36': uidb36})
        self.assertIsNotNone(url)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
