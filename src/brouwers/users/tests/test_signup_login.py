# -*- coding: UTF-8 -*-
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django_webtest import WebTest

from brouwers.forum_tools.tests.factory_models import ForumUserFactory
from brouwers.general.tests.factory_models import RegistrationQuestionFactory

from .factories import UserFactory


class LoginRegisterTests(WebTest):
    # TODO:
    #   - succesful registration
    #   - test e-mail suspicous registration and not logged in
    #   - test registration logging
    #   - test registration e-mail is sent
    def setUp(self):
        username = "My user"
        self.user = UserFactory(username=username)
        self.forum_user = ForumUserFactory(username=username)

    def test_login(self):
        """ Test that we can log in with the forum name containing spaces """
        # production -> redirect to php index
        response = self.client.get("/")
        # we don't serve php obviously, so 404 is expected
        self.assertRedirects(response, "/index.php", target_status_code=404)

        # test login
        response = self.client.get(settings.LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["form"])

        post_data = {
            "username": self.forum_user.username,
            "password": "password",
            "next": "/index.php",
        }
        response = self.client.post(settings.LOGIN_URL, post_data)
        # redirects
        self.assertRedirects(response, "/index.php", target_status_code=404)
        self.assertIn("_auth_user_id", self.client.session)

    def test_email_login(self):
        """ Test that we can also login with the e-mail address """
        post_data = {
            "username": self.user.email,
            "password": "password",
            "next": "/index.php",
        }
        response = self.client.post(settings.LOGIN_URL, post_data)
        self.assertRedirects(response, "/index.php", target_status_code=404)
        self.assertIn("_auth_user_id", self.client.session)

    def test_email_not_logged_in_duplicate(self):
        """ Test that duplicate e-mail users are not logged in """
        user2 = UserFactory(email=self.user.email)
        self.assertEqual(user2.email, self.user.email)

        post_data = {
            "username": self.user.email,
            "password": "password",
            "next": "/index.php",
        }
        response = self.client.post(settings.LOGIN_URL, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    def test_register(self):
        url = reverse("users:register")

        # create a registration question that has to be answered
        question = RegistrationQuestionFactory.create(lang="en")
        answer = "answer"  # default answer from the factory model

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            "username": "My user2",
            "email": "myuser@dummy.com",
            "password1": "password",
            "password2": "password",
            "question": question.id,
            "answer": answer,
            "accept_terms": True,
        }

        response = self.client.post(url, post_data)
        # test that the registration was succesful and a redirect
        # to the profile occurs
        self.assertRedirects(response, "/profile/")
        # test that the user is logged in
        self.assertIn("_auth_user_id", self.client.session)

        # test that we are effectively able to log in
        self.client.logout()
        self.assertNotIn("_auth_user_id", self.client.session)
        self.client.login(username="My user2", password="password")
        self.assertIn("_auth_user_id", self.client.session)

    def test_register_no_question_submitted(self):
        url = reverse("users:register")

        # create a registration question that has to be answered
        RegistrationQuestionFactory.create(lang="en")
        answer = "answer"  # default answer from the factory model

        post_data = {
            "username": "My user2",
            "email": "myuser@dummy.com",
            "password1": "password",
            "password2": "password",
            "answer": answer,
            "accept_terms": True,
        }

        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "question", [_("This field is required.")]
        )

    def test_username_case_insensitive(self):
        """
        Test that duplicate usernames (case insensitive) trigger form validation.
        """
        RegistrationQuestionFactory.create(lang="en")
        UserFactory.create(username="John Doe")

        registration = self.app.get(reverse("users:register"))
        self.assertEqual(registration.status_code, 200)

        form = registration.form
        form["username"] = "john doe"
        form["email"] = "myuser@dummy.com"
        form["password1"] = "secret"
        form["password2"] = "secret"
        form["answer"] = "answer"

        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "username", _("A user with that username already exists.")
        )

    def test_login_username_case_insensitive(self):
        UserFactory.create(username="Rodith", password="letmein")

        login_page = self.app.get(settings.LOGIN_URL)
        login_page.form["username"] = "rodith"
        login_page.form["password"] = "letmein"

        response = login_page.form.submit()

        self.assertEqual(response.status_code, 302)

    def test_login_username_same_email(self):
        UserFactory.create(
            username="FOO@bar.com", email="foo@bar.com", password="letmein"
        )

        login_page = self.app.get(settings.LOGIN_URL)
        login_page.form["username"] = "foo@bar.com"
        login_page.form["password"] = "letmein"

        response = login_page.form.submit()

        self.assertEqual(response.status_code, 302)

    def test_register_invisible_if_logged_in(self):
        """ Test that the registration page is not accessible if the user is logged in"""
        url = "/register/"
        self.client.login(username=self.user.username, password="password")
        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.get(url)
        self.assertRedirects(response, "/", target_status_code=302)


class RegistrationTests(TestCase):
    def setUp(self):
        self.UserModel = UserFactory._meta.model
        self.url = "/register/"

    def test_anti_spambot_question(self):
        """ Test that wrong answers block registration """
        self.assertEqual(self.UserModel.objects.count(), 0)

        question = RegistrationQuestionFactory.create(lang="en")
        answer = "not-answer"  # 'answer' is the default answer from the factory model

        post_data = {
            "username": "My user2",
            "email": "myuser@dummy.com",
            "password1": "password",
            "password2": "password",
            "question": question.id,
            "answer": answer,
        }

        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        # Test that no user account was created
        self.assertEqual(self.UserModel.objects.count(), 0)


class LogoutTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.logout_url = "/logout/"

    def test_logout_authenticated(self):
        self.client.login(username=self.user.username, password="password")
        response = self.client.get(self.logout_url)
        self.assertRedirects(
            response, "/", target_status_code=302
        )  # / issues a redirect to /index.php
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_not_authenticated(self):
        # not logged in, should just work too
        response = self.client.get(self.logout_url)
        self.assertRedirects(
            response, "/", target_status_code=302
        )  # / issues a redirect to /index.php
        self.assertNotIn("_auth_user_id", self.client.session)
