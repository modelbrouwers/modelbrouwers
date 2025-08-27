from django.core import mail
from django.db import connections
from django.urls import reverse

from django_webtest import WebTest

from brouwers.utils.tests.recaptcha import mock_recaptcha

from ..models import ContactMessage


class SubmitContactMessageTests(WebTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # it's SQlite in tests, if this breaks -> update your databases setting in
        # local.py
        with connections["legacy_shop"].cursor() as cursor:
            sql = """
                CREATE TABLE IF NOT EXISTS oc_setting (
                  "setting_id" INTEGER NOT NULL PRIMARY KEY,
                  "store_id" INTEGER NOT NULL DEFAULT 0,
                  "group" TEXT NOT NULL,
                  "key" TEXT NOT NULL,
                  "value" TEXT NOT NULL,
                  "serialized" INTEGER NOT NULL
                )
            """
            cursor.execute(sql)

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

            msg = mail.outbox[0]

            self.assertEqual(msg.reply_to, ["donald@disney.com"])
            self.assertIn("Quack quack quack\nBest, Dolan", msg.body)
