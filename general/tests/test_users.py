# -*- coding: UTF-8 -*-
from django.conf import settings
from django.test import TestCase

from forum_tools.tests.factory_models import ForumUserFactory
from general.utils import get_username, clean_username, clean_username_fallback

from .factory_models import UserFactory, RegistrationQuestionFactory


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
        self.assertEqual(clean_username(username), u'myʹuser')
        self.assertEqual(clean_username_fallback(username), 'my user')


class LoginTestCase(TestCase):
    def setUp(self):
        username = 'My user'
        self.user = UserFactory(username=username)
        self.forum_user = ForumUserFactory(username=username)

    def test_login(self):
        """ Test that we can log in with the forum name containing spaces """
        # production -> redirect to php index
        response = self.client.get('/')
        self.assertRedirects(response, '/index.php', target_status_code=404) # we don't serve php obviously

        # test login
        response = self.client.get(settings.LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])

        post_data = {
            'username': self.forum_user.username,
            'password': 'password',
            'next': '/index.php',
        }
        response = self.client.post(settings.LOGIN_URL, post_data)
        # redirects
        self.assertRedirects(response, '/index.php', target_status_code=404)

    def test_register(self):
        url = '/register/'

        # create a registration question that has to be answered
        question = RegistrationQuestionFactory()
        answer = 'answer' # default answer from the factory model

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            'forum_nickname': 'My user2',
            'email': 'myuser@dummy.com',
            'password1': 'password',
            'password2': 'password',
            'question': question.id,
            'answer': answer
        }

        response = self.client.post(url, post_data)
        # test that the registration was succesful and a redirect
        # to the profile occurs
        self.assertRedirects(response, '/profile/')
        # test that the user is logged in
        self.assertIn('_auth_user_id', self.client.session)
