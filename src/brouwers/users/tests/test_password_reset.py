from django.core import mail
from django.urls import reverse

from django_webtest import WebTest

from .factories import UserFactory


class PasswordResetTests(WebTest):
    def test_password_reset_request_email(self):
        UserFactory.create(email="foo@bar.com")
        url = reverse("users:pw_reset")

        response = self.app.get(url)

        form = response.form
        form["email"] = "foo@bar.com"
        result = form.submit()

        self.assertEqual(result.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

    def test_password_reset_request_username(self):
        UserFactory.create(email="foo@bar.com", username="santa")
        url = reverse("users:pw_reset")

        response = self.app.get(url)

        form = response.form
        form["username"] = "santa"
        result = form.submit()

        self.assertEqual(result.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
