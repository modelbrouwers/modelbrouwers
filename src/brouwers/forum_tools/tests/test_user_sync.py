from django.test import TestCase

from brouwers.users.tests.factory_models import UserFactory
from .factory_models import ForumUserFactory


class UserSyncTests(TestCase):

    def test_email(self):
        email = 'email1@test.com'
        forum_user = ForumUserFactory(username='test', user_email=email)
        user = UserFactory(email=email, forumuser_id=forum_user.pk)
        self.assertEqual(user.email, forum_user.user_email)
        self.assertIsNotNone(user.forumuser)

        user.email = 'email2@test.com'
        user.save()
        self.assertEqual(user.email, user.forumuser.user_email)

    def test_lookup_user(self):
        """
        In case that no forum user ID was set on the user, try to look up the
        forum user by name.
        """
        email = 'email1@test.com'
        forum_user = ForumUserFactory(username='test', user_email=email)
        user = UserFactory(username='test', email=email)
        self.assertEqual(user.forumuser, forum_user)

        # test with non-existant forum user
        user2 = UserFactory(username='test2')
        self.assertIsNone(user2.forumuser)
