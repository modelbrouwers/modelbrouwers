from django.urls import reverse

from django_webtest import WebTest
from webtest import Upload

from brouwers.users.tests.factories import UserFactory

from ...models import Product
from ..factories import ProductFactory


class ProductAdminTests(WebTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = UserFactory.create(superuser=True)

    def setUp(self):
        super().setUp()
        self.app.set_user(self.user)

    def test_export_import_roundtrip(self):
        ProductFactory.create_batch(10)
        export_page = self.app.get(reverse("admin:shop_product_export"))
        export_form = export_page.forms[1]
        export_form["format"].select(text="json")
        export_response = export_form.submit()
        assert export_response.status_code == 200
        json_data: bytes = export_response.content
        Product.objects.all().delete()

        # import the export file again
        import_page = self.app.get(reverse("admin:shop_product_import"))
        import_form = import_page.forms[1]
        import_form["import_file"] = Upload(
            "export.json", json_data, "application/json"
        )
        import_form["format"].select(text="json")
        import_response = import_form.submit()
        preview_table = import_response.pyquery("table.import-preview")
        self.assertTrue(preview_table)
        confirm_form = import_response.forms[1]
        confirm_response = confirm_form.submit()
        self.assertEqual(confirm_response.status_code, 302)
        self.assertEqual(Product.objects.count(), 10)
