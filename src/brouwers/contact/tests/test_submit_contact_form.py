from django.core import mail
from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest

from brouwers.utils.tests.recaptcha import mock_recaptcha

from ..models import ContactMessage


class SubmitContactMessageTests(WebTest):
    @mock_recaptcha(is_valid=True, action="contact")
    def test_submit_valid_message(self, m):
        url = reverse("contact")
        contact_page = self.app.get(url)
        form = contact_page.forms["contact"]

        form["name"] = "Donald Duck"
        form["email"] = "donald@disney.com"
        form["message"] = "Quack quack quack\nBest, Dolan"
        form["captcha"] = "dummy"
        with self.captureOnCommitCallbacks(execute=True):
            response = form.submit()

        self.assertEqual(response.status_code, 302)

        with self.subTest("Message saved in DB"):
            self.assertTrue(ContactMessage.objects.exists())
            message = ContactMessage.objects.get()
            self.assertEqual(message.name, "Donald Duck")
            self.assertEqual(message.email, "donald@disney.com")
            self.assertEqual(message.message, "Quack quack quack\nBest, Dolan")

        with self.subTest("Notification email"):
            self.assertEqual(len(mail.outbox), 1)
