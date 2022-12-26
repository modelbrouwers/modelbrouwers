from django.test import override_settings
from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ...models import PaymentMethod


@override_settings(LANGUAGE_CODE="nl")
class PaymentMethodAdminTests(WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = UserFactory.create(superuser=True)

    def test_add_payment_method(self):
        self.app.set_user(self.user)

        with self.subTest("add a payment method"):
            url = reverse("admin:shop_paymentmethod_add")
            add_page = self.app.get(url)
            add_form = add_page.forms["paymentmethod_form"]

            add_form["name_nl"] = "Test method"
            add_form["method"].select("sisow_ideal")
            add_form["enabled"] = True

            add_form.submit()

            methods = PaymentMethod.objects.all()
            self.assertEqual(methods.count(), 1)

        with self.subTest("list payment methods"):
            url = reverse("admin:shop_paymentmethod_changelist")

            changelist = self.app.get(url)

            self.assertInHTML("Test method", changelist.text)
