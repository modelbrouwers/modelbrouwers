import os

from django.test import tag
from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest
from webtest.forms import Select, Text

from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.vcr import VCRMixin, VCRTestCase

from ..models import ShopConfiguration
from ..sendcloud import Client
from .factories import SendcloudShippingOptionFactory


class SendcloudClientTests(VCRTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        config = ShopConfiguration.get_solo()
        config.sendcloud_public_key = os.getenv("SENDCLOUD_API_KEY", "")
        config.sendcloud_private_key = os.getenv("SENDCLOUD_API_SECRET", "")
        config.save()
        cls.addClassCleanup(config.clear_cache)

    def test_create_shipment_label(self):
        SendcloudShippingOptionFactory.create(country="N")

        with Client() as client:
            result = client.create_shipping_label(
                customer_name="Hanjos",
                street="Voorstraat",
                number="18",
                postal_code="2964AK",
                city="Groot-Ammers",
                country="N",
                weight_in_grams=513,
            )

            # cancel the shipment to avoid potential costs!
            client.cancel_shipment(id=result.id)

        self.assertGreater(len(result.id), 0)
        self.assertGreater(len(result.label_file), 0)
        self.assertEqual(result.label_ext, ".pdf")
        self.assertGreater(len(result.tracking_number), 0)
        self.assertGreater(len(result.tracking_url), 0)

    def test_create_shipment_label_weight_in_kg(self):
        SendcloudShippingOptionFactory.create(country="D")

        with Client() as client:
            result = client.create_shipping_label(
                customer_name="Hanjos",
                street="Schönwalder Allee 6",
                number="6",
                postal_code="93451",
                city="City:  Neukirchen",
                country="D",
                weight_in_grams=1200,
            )

            # cancel the shipment to avoid potential costs!
            client.cancel_shipment(id=result.id)

        self.assertGreater(len(result.id), 0)
        self.assertGreater(len(result.label_file), 0)
        self.assertEqual(result.label_ext, ".pdf")
        self.assertGreater(len(result.tracking_number), 0)
        self.assertGreater(len(result.tracking_url), 0)


@tag("vcr")
class AdminConfigurationTests(VCRMixin, WebTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = UserFactory.create(superuser=True)

    def test_can_save_without_sendcloud_credentials_configured(self):
        change_page = self.app.get(
            reverse("admin:shop_shopconfiguration_change", args=(1,)),
            user=self.user,
        )
        form = change_page.forms["shopconfiguration_form"]
        form["bank_transfer_instructions_nl"] = "dummy"
        assert form["sendcloud_public_key"].value == ""
        assert form["sendcloud_private_key"].value == ""

        response = form.submit()

        self.assertEqual(response.status_code, 302)

    def test_configure_sendcloud_credentials(self):
        change_page = self.app.get(
            reverse("admin:shop_shopconfiguration_change", args=(1,)),
            user=self.user,
        )
        form = change_page.forms["shopconfiguration_form"]
        form["bank_transfer_instructions_nl"] = "dummy"

        with self.subTest("invalid credentials"):
            form["sendcloud_public_key"] = "wrong-value"
            form["sendcloud_private_key"] = "wrong-value"

            response = form.submit()

            self.assertEqual(response.status_code, 200)
            self.assertFormError(
                response.context["adminform"].form,
                None,
                errors=_("The Sendcloud credentials don't appear to be valid."),
            )

        with self.subTest("valid credentials"):
            form["sendcloud_public_key"] = os.getenv(
                "SENDCLOUD_API_KEY", "dummy-for-ci"
            )
            form["sendcloud_private_key"] = os.getenv(
                "SENDCLOUD_API_SECRET", "dummy-for-ci"
            )

            response = form.submit()

            self.assertEqual(response.status_code, 302)
            config = ShopConfiguration.get_solo()
            self.assertNotEqual(config.sendcloud_public_key, "")
            self.assertNotEqual(config.sendcloud_private_key, "")

    def test_configure_shipping_option_entry_uses_charfield(self):
        add_url = reverse("admin:shop_sendcloudshippingoption_add")
        self.app.set_user(self.user)

        with self.subTest(
            "new shipping options without sendclound credentials configured"
        ):
            add_page = self.app.get(add_url)
            add_form = add_page.forms["sendcloudshippingoption_form"]

            self.assertEqual(add_form["country"].value, "")
            self.assertNotEqual(add_form["shipping_option_code"].value, "")
            self.assertIsInstance(add_form["shipping_option_code"], Text)

        with self.subTest(
            "existing shipping options without sendclound credentials configured"
        ):
            shipping_option = SendcloudShippingOptionFactory.create(country="N")
            change_url = reverse(
                "admin:shop_sendcloudshippingoption_change", args=(shipping_option.pk,)
            )

            change_page = self.app.get(change_url)
            change_form = change_page.forms["sendcloudshippingoption_form"]

            self.assertEqual(change_form["country"].value, "N")
            self.assertNotEqual(change_form["shipping_option_code"].value, "")
            self.assertIsInstance(change_form["shipping_option_code"], Text)

        config = ShopConfiguration.get_solo()
        config.sendcloud_public_key = os.getenv("SENDCLOUD_API_KEY", "dummy-for-ci")
        config.sendcloud_private_key = os.getenv("SENDCLOUD_API_SECRET", "dummy-for-ci")
        config.save()
        self.addCleanup(config.clear_cache)

        with self.subTest("new shipping option with credentials configured"):
            add_page = self.app.get(add_url)
            add_form = add_page.forms["sendcloudshippingoption_form"]

            self.assertEqual(add_form["country"].value, "")
            self.assertNotEqual(add_form["shipping_option_code"].value, "")
            self.assertIsInstance(add_form["shipping_option_code"], Text)

    def test_configure_shipping_option_entry_uses_dropdown(self):
        config = ShopConfiguration.get_solo()
        config.sendcloud_public_key = os.getenv("SENDCLOUD_API_KEY", "dummy-for-ci")
        config.sendcloud_private_key = os.getenv("SENDCLOUD_API_SECRET", "dummy-for-ci")
        config.save()
        self.addCleanup(config.clear_cache)

        shipping_option = SendcloudShippingOptionFactory.create(country="B")
        change_url = reverse(
            "admin:shop_sendcloudshippingoption_change", args=(shipping_option.pk,)
        )

        change_page = self.app.get(change_url, user=self.user)
        change_form = change_page.forms["sendcloudshippingoption_form"]

        self.assertEqual(change_form["country"].value, "B")
        self.assertNotEqual(change_form["shipping_option_code"].value, "")
        self.assertIsInstance(change_form["shipping_option_code"], Select)

    def test_configure_shipping_option_entry_uses_textfield_if_sendcloud_api_errors(
        self,
    ):
        config = ShopConfiguration.get_solo()
        config.sendcloud_public_key = os.getenv("SENDCLOUD_API_KEY", "dummy-for-ci")
        config.sendcloud_private_key = os.getenv("SENDCLOUD_API_SECRET", "dummy-for-ci")
        config.save()
        self.addCleanup(config.clear_cache)

        shipping_option = SendcloudShippingOptionFactory.create(country="B")
        change_url = reverse(
            "admin:shop_sendcloudshippingoption_change", args=(shipping_option.pk,)
        )

        with self.vcr_raises():
            change_page = self.app.get(change_url, user=self.user)
        change_form = change_page.forms["sendcloudshippingoption_form"]

        self.assertEqual(change_form["country"].value, "B")
        self.assertNotEqual(change_form["shipping_option_code"].value, "")
        self.assertIsInstance(change_form["shipping_option_code"], Text)
