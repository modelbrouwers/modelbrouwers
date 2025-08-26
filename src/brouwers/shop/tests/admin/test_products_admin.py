import json

from django.urls import reverse
from django.utils.translation import gettext as _

from django_webtest import WebTest
from taggit.models import Tag, TaggedItem
from webtest import Upload

from brouwers.users.tests.factories import UserFactory

from ...models import Product
from ..factories import CategoryFactory, ProductFactory, ProductManufacturerFactory


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

    def test_export_with_relations(self):
        p1, p2, p3 = ProductFactory.create_batch(3)
        c1, c2, c3 = CategoryFactory.create_batch(3)
        p1.categories.add(c1, c2)
        p2.categories.add(c3)
        TaggedItem.objects.create(
            tag=Tag.objects.create(name="a tag"), content_object=p2
        )
        p3.related_products.add(p1)

        export_page = self.app.get(reverse("admin:shop_product_export"))
        export_form = export_page.forms[1]
        export_form["format"].select(text="json")
        export_response = export_form.submit()
        assert export_response.status_code == 200
        export_data = export_response.json_body

        exported_products = sorted(export_data, key=lambda i: int(i["id"]))
        assert exported_products[0]["id"] == str(p1.pk)
        assert exported_products[1]["id"] == str(p2.pk)
        assert exported_products[2]["id"] == str(p3.pk)

        with self.subTest("categories"):
            self.assertEqual(
                set(exported_products[0]["categories"].split(",")),
                {str(c1.pk), str(c2.pk)},
            )
            self.assertEqual(
                set(exported_products[1]["categories"].split(",")),
                {str(c3.pk)},
            )

        with self.subTest("tags"):
            self.assertEqual(exported_products[1]["tags"], '"a tag"')

        with self.subTest("related products"):
            self.assertEqual(exported_products[2]["related_products"], str(p1.pk))

    def test_import_minimal_fields(self):
        import_data = json.dumps(
            [
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                }
            ]
        )
        import_page = self.app.get(reverse("admin:shop_product_import"))
        import_form = import_page.forms[1]
        import_form["import_file"] = Upload(
            "export.json", import_data.encode("utf-8"), "application/json"
        )
        import_form["format"].select(text="json")

        import_response = import_form.submit()

        preview_table = import_response.pyquery("table.import-preview")
        self.assertTrue(preview_table)
        confirm_form = import_response.forms[1]
        confirm_response = confirm_form.submit()
        self.assertEqual(confirm_response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)

    def test_import_with_manufacturer(self):
        manufacturer = ProductManufacturerFactory.create()
        import_data = json.dumps(
            [
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                    "manufacturer": str(manufacturer.pk),
                }
            ]
        )
        import_page = self.app.get(reverse("admin:shop_product_import"))
        import_form = import_page.forms[1]
        import_form["import_file"] = Upload(
            "export.json", import_data.encode("utf-8"), "application/json"
        )
        import_form["format"].select(text="json")

        import_response = import_form.submit()
        confirm_form = import_response.forms[1]
        confirm_response = confirm_form.submit()

        self.assertEqual(confirm_response.status_code, 302)
        product = Product.objects.get()
        self.assertEqual(product.manufacturer, manufacturer)

    def test_import_with_categories(self):
        CategoryFactory.create(name="first")
        category_2 = CategoryFactory.create(name="second")
        category_3 = CategoryFactory.create(name="third")

        import_data = json.dumps(
            [
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                    "manufacturer": "",
                    "categories": f"{category_2.pk},{category_3.pk}",
                }
            ]
        )
        import_page = self.app.get(reverse("admin:shop_product_import"))
        import_form = import_page.forms[1]
        import_form["import_file"] = Upload(
            "export.json", import_data.encode("utf-8"), "application/json"
        )
        import_form["format"].select(text="json")

        import_response = import_form.submit()
        confirm_form = import_response.forms[1]
        confirm_response = confirm_form.submit()

        self.assertEqual(confirm_response.status_code, 302)
        product = Product.objects.get()
        self.assertQuerySetEqual(
            product.categories.values_list("pk", flat=True),
            {category_2.pk, category_3.pk},
            ordered=False,
        )

    def test_import_with_tags(self):
        import_data = json.dumps(
            [
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                    "tags": 'Tag One, tag two, "tag,with,commas"',
                }
            ]
        )
        import_page = self.app.get(reverse("admin:shop_product_import"))
        import_form = import_page.forms[1]
        import_form["import_file"] = Upload(
            "export.json", import_data.encode("utf-8"), "application/json"
        )
        import_form["format"].select(text="json")

        import_response = import_form.submit()
        confirm_form = import_response.forms[1]
        confirm_response = confirm_form.submit()

        self.assertEqual(confirm_response.status_code, 302)
        product = Product.objects.get()
        self.assertQuerySetEqual(
            product.tags.values_list("name", flat=True),
            {"Tag One", "tag two", "tag,with,commas"},
            ordered=False,
        )

    def test_import_with_related_products(self):
        product1, product2 = ProductFactory.create_batch(2)
        import_data = json.dumps(
            [
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                    "related_products": f"{product1.pk},{product2.pk}",
                }
            ]
        )
        import_page = self.app.get(reverse("admin:shop_product_import"))
        import_form = import_page.forms[1]
        import_form["import_file"] = Upload(
            "export.json", import_data.encode("utf-8"), "application/json"
        )
        import_form["format"].select(text="json")

        import_response = import_form.submit()
        confirm_form = import_response.forms[1]
        confirm_response = confirm_form.submit()

        self.assertEqual(confirm_response.status_code, 302)
        created_product = Product.objects.order_by("-pk").first()
        assert created_product is not None
        self.assertQuerySetEqual(
            created_product.related_products.all(),
            [product1, product2],
            ordered=False,
            transform=lambda p: p,
        )

    def test_import_with_invalid_datatypes(self):
        import_data = json.dumps(
            [
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                    "categories": "a,b",
                    "tags": "",
                    "related_products": "",
                },
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                    "categories": "",
                    "tags": '"unclosed quote',
                    "related_products": "",
                },
                {
                    "id": "",
                    "name": "My product",
                    "slug": "",
                    "model_name": "Awesome thing",
                    "stock": "",
                    "price": "",
                    "vat": "",
                    "description": "",
                    "meta_description": "",
                    "length": "",
                    "width": "",
                    "height": "",
                    "weight": "",
                    "categories": "",
                    "tags": "",
                    "related_products": "a,b",
                },
            ]
        )
        import_page = self.app.get(reverse("admin:shop_product_import"))
        import_form = import_page.forms[1]
        import_form["import_file"] = Upload(
            "export.json", import_data.encode("utf-8"), "application/json"
        )
        import_form["format"].select(text="json")

        import_response = import_form.submit()

        with self.subTest("categories"):
            self.assertContains(
                import_response,
                _("Categories must be a comma separated list of database IDs."),
            )

        with self.subTest("related products"):
            self.assertContains(
                import_response,
                _("Related products must be a comma separated list of database IDs."),
            )
