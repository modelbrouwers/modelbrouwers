"""
Tests the integration with linked models like ForumUser and UserProfile
"""

from django.test import TestCase

from brouwers.forum_tools.tests.factories import create_from_user

from .factories import UserFactory


class LinkedModelsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.forum_user = create_from_user(self.user)

    def test_username_changes(self):
        """If the username changes, test that the forumprofile and forumuser change"""
        self.assertEqual(self.user.username, self.forum_user.username)
        self.assertIsNotNone(self.user.profile)
        self.assertEqual(self.user.profile.forum_nickname, self.forum_user.username)

        new_username = "changed username"

        self.user.username = new_username
        self.user.save()

        # refresh user instance
        user = self.user.__class__._default_manager.get(pk=self.user.pk)
        self.assertEqual(user.username, new_username)
        self.assertEqual(user.forumuser.username, new_username)
        self.assertEqual(user.profile.forum_nickname, new_username)
