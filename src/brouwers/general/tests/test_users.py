# -*- coding: UTF-8 -*-
from django.test import TestCase

from brouwers.general.utils import (
    clean_username, clean_username_fallback, get_username
)


class UsernameTest(TestCase):
    def setUp(self):
        class User(object):
            def __init__(self, username):
                super().__init__()
                self.username = username

        class TestObject(object):
            def __init__(self, username):
                super().__init__()
                self.field = User(username)
                self.user = User(username)

        self.object1 = TestObject('BBT')
        self.object2 = TestObject('Joe_Silent')
        self.object3 = TestObject('My\'User')

    def test_username_correct(self):
        """
        Tests that underscores are converted to spaces
        """
        self.assertEqual(get_username(self.object1, field='field'), 'BBT')
        self.assertEqual(get_username(self.object2, field='field'), 'Joe Silent')
        self.assertEqual(get_username(self.object2), 'Joe Silent')

    def test_clean_username(self):
        username = self.object3.user.username
        self.assertEqual(clean_username(username), u'myʹuser')
        self.assertEqual(clean_username_fallback(username), 'my user')
