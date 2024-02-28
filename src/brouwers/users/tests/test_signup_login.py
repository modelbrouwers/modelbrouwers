from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from django_webtest import WebTest

from brouwers.forum_tools.tests.factory_models import ForumUserFactory
from brouwers.utils.tests.recaptcha import mock_recaptcha

from .factories import UserFactory


class LoginRegisterTests(WebTest):
    def setUp(self):
        super().setUp()

        username = "My user"
        self.user = UserFactory(username=username)
        self.forum_user = ForumUserFactory(username=username)

    @mock_recaptcha(is_valid=True, action="login")
    def test_login(self, m):
        """Test that we can log in with the forum name containing spaces"""
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
            "captcha": "dummy",
        }
        response = self.client.post(settings.LOGIN_URL, post_data)
        # redirects
        self.assertRedirects(response, "/index.php", target_status_code=404)
        self.assertIn("_auth_user_id", self.client.session)

    @mock_recaptcha(is_valid=True, action="login")
    def test_email_login(self, m):
        """Test that we can also login with the e-mail address"""
        post_data = {
            "username": self.user.email,
            "password": "password",
            "next": "/index.php",
            "captcha": "dummy",
        }
        response = self.client.post(settings.LOGIN_URL, post_data)
        self.assertRedirects(response, "/index.php", target_status_code=404)
        self.assertIn("_auth_user_id", self.client.session)

    @mock_recaptcha(is_valid=True, action="login")
    def test_login_email_longer_than_30_chars_possible(self, m):
        user = UserFactory.create(
            email="i-am-longer-than-30-characters@example.com", password="so-secret"
        )

        login_page = self.app.get(settings.LOGIN_URL)
        login_form = login_page.form

        with self.subTest("No length limit on username field"):
            self.assertNotIn("maxlength", login_form["username"].attrs)

        with self.subTest("logging in with credentials"):
            login_form["username"] = "i-am-longer-than-30-characters@example.com"
            login_form["password"] = "so-secret"
            login_form["captcha"] = "dummy"

            response = login_form.submit()

            self.assertEqual(response.status_code, 302)
            user_id = int(self.app.session["_auth_user_id"])
            self.assertEqual(user_id, user.id)

    @mock_recaptcha(is_valid=True, action="login")
    def test_email_not_logged_in_duplicate(self, m):
        """Test that duplicate e-mail users are not logged in"""
        user2 = UserFactory(email=self.user.email)
        self.assertEqual(user2.email, self.user.email)

        post_data = {
            "username": self.user.email,
            "password": "password",
            "next": "/index.php",
            "captcha": "dummy",
        }
        response = self.client.post(settings.LOGIN_URL, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    @mock_recaptcha(is_valid=True, action="signup")
    def test_register(self, m):
        url = reverse("users:register")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            "username": "My user2",
            "email": "myuser@dummy.com",
            "password1": "password",
            "password2": "password",
            "accept_terms": True,
            "captcha": "dummy",
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

    def test_register_no_captcha_submitted(self):
        url = reverse("users:register")

        post_data = {
            "username": "My user2",
            "email": "myuser@dummy.com",
            "password1": "password",
            "password2": "password",
            "accept_terms": True,
        }

        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "captcha", [str(_("This field is required."))]
        )

    @mock_recaptcha(is_valid=True, action="signup")
    def test_registration_username_case_insensitive(self, m):
        """
        Test that duplicate usernames (case insensitive) trigger form validation.
        """
        UserFactory.create(username="John Doe")

        registration = self.app.get(reverse("users:register"))
        self.assertEqual(registration.status_code, 200)

        form = registration.form
        form["username"] = "john doe"
        form["email"] = "myuser@dummy.com"
        form["password1"] = "secret"
        form["password2"] = "secret"
        form["captcha"] = "dummy"

        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            str(_("A user with that username already exists.")),
        )

    @mock_recaptcha(is_valid=True, action="login")
    def test_login_username_case_insensitive(self, m):
        UserFactory.create(username="Rodith", password="letmein")

        login_page = self.app.get(settings.LOGIN_URL)
        login_page.form["username"] = "rodith"
        login_page.form["password"] = "letmein"
        login_page.form["captcha"] = "dummy"

        response = login_page.form.submit()

        self.assertEqual(response.status_code, 302)

    @mock_recaptcha(is_valid=True, action="login")
    def test_login_username_same_email(self, m):
        UserFactory.create(
            username="FOO@bar.com", email="foo@bar.com", password="letmein"
        )

        login_page = self.app.get(settings.LOGIN_URL)
        login_page.form["username"] = "foo@bar.com"
        login_page.form["password"] = "letmein"
        login_page.form["captcha"] = "dummy"

        response = login_page.form.submit()

        self.assertEqual(response.status_code, 302)

    def test_register_invisible_if_logged_in(self):
        """Test that the registration page is not accessible if the user is logged in"""
        url = "/register/"
        self.client.login(username=self.user.username, password="password")
        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.get(url)
        self.assertRedirects(response, "/", target_status_code=302)


class LogoutTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()
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
