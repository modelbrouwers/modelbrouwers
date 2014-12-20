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
