from django.test import TestCase

from brouwers.forum_tools.tests.factory_models import ForumUserFactory
from ..tokens import activation_token_generator
from .factories import UserFactory


class ActivationTokenTests(TestCase):
    def setUp(self):
        self.forum_user = ForumUserFactory()
        self.user = UserFactory(forumuser_id=self.forum_user.user_id, is_active=False)
        self.user2 = UserFactory(forumuser_id=self.forum_user.user_id, is_active=False)

    def test_token_inactive(self):
        """ Test that the tokens return expected compare failures/successes """

        # self.user is not activated
        self.assertIsNotNone(self.user.forumuser_id)
        self.assertFalse(self.user.is_active)

        token = activation_token_generator.make_token(self.user)
        self.assertIsNotNone(token)
        # compare the tokens
        self.assertTrue(activation_token_generator.check_token(self.user, token))

        # test that a token for a different user with the same forum account is invalid
        token2 = activation_token_generator.make_token(self.user2)
        self.assertFalse(activation_token_generator.check_token(self.user, token2))

    def test_token_active(self):
        """ Test that token is invalid if the user is activated """
        token = activation_token_generator.make_token(self.user)
        self.user.is_active = True
        self.assertFalse(activation_token_generator.check_token(self.user, token))

    def test_malformatted_token(self):
        token = 'abcfoobar'
        self.assertFalse(activation_token_generator.check_token(self.user, token))
