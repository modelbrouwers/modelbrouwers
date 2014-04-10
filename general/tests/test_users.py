# -*- coding: UTF-8 -*-
from django.conf import settings
from django.test import TestCase

from forum_tools.tests.factory_models import ForumUserFactory
from general.utils import get_username, clean_username, clean_username_fallback

from .factory_models import UserFactory


class UsernameTest(TestCase):
    def setUp(self):
        class User(object):
            def __init__(self, username):
                super(User, self).__init__()
                self.username = username

        class TestObject(object):
            def __init__(self, username):
                super(TestObject, self).__init__()
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
        self.assertEqual(clean_username(username), 'myʹuser')
        self.assertEqual(clean_username_fallback(username), 'my user')


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username='my_user')
        self.forum_user = ForumUserFactory()

    def test_login(self):
        """ Test that we can log in with the forum name containing spaces """
        # production -> redirect to php index
        response = self.client.get('/')
        self.assertRedirects(response, '/index.php', target_status_code=404) # we don't serve php obviously

        # test login
        response = self.client.get(settings.LOGIN_URL)
        self.assertEqual(response.status_code, 200)