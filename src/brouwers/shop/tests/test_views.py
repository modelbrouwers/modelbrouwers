import uuid

from django.template import engines
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext as _, override

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ..models import Category
from .factories import CartFactory, CategoryFactory, ProductFactory


class BreadcrumbsTests(TestCase):
    def _load_template(self, tpl):
        return engines["django"].from_string(tpl)

    def test_breadcrumbs_render(self):
        """
        Asserts that breadcrumbs are rendered correctly.
        """
        self.maxDiff = None
        tpl = "{% include 'shop/includes/breadcrumbs.html' with curr_node=node%}"
        template = self._load_template(tpl)

        root = Category.add_root(name="Root")
        child1 = root.add_child(name="Child1")
        child1.save()
        child2 = child1.add_child(name="Child2")
        child2.save()

        rendered = template.render({"node": child2})
        self.assertHTMLEqual(
            rendered,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/root">Root</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/root/child1">Child1</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/root/child1/child2">Child2</a></div>',
        )

        rendered2 = template.render({"node": child1})
        self.assertHTMLEqual(
            rendered2,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/root">Root</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/root/child1">Child1</a>',
        )

        rendered3 = template.render({"node": root})
        self.assertHTMLEqual(
            rendered3,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/root">Root</a>',
        )


class CartViewTests(WebTest):
    def setUp(self):
        self.user = UserFactory.create()
        self.cart = CartFactory.create(user=self.user)
        self.url = reverse("shop:cart-detail", kwargs={"pk": self.cart.id})

    def test_cart_detail_view(self):
        """
        Asserts that cart detail view is properly loaded and available only to the cart user
        """
        cart_page = self.app.get(self.url, user=self.user)
        self.assertEqual(cart_page.status_code, 200)
        cart = cart_page.context["cart"]
        self.assertEqual(cart, self.cart)

        # Check that other users can't view the same cart

        second_user = UserFactory.create()
        cart_page = self.app.get(self.url, user=second_user, expect_errors=True)
        self.assertEqual(cart_page.status_code, 404)


class CatalogueRouterTests(TestCase):
    def test_dynamic_routing(self):
        category = CategoryFactory.create(slug="root")
        ProductFactory.create(slug="a-product", categories=[category])

        bad_urls = (
            "/not-root",
            "/not-product",
            "/root/not a proper slug",
        )

        for bad_url in bad_urls:
            with self.subTest(bad_url=bad_url):
                response = self.client.get(f"/winkel{bad_url}")

                self.assertEqual(response.status_code, 404)

        good_urls = (
            ("/root", "shop/category_detail.html"),
            ("/random/root", "shop/category_detail.html"),
            ("/a-product", "shop/product_detail.html"),
            ("/root/a-product", "shop/product_detail.html"),
            ("/nonsense/a-product", "shop/product_detail.html"),
        )

        for good_url, template_name in good_urls:
            with self.subTest(good_url=good_url):
                response = self.client.get(f"/winkel{good_url}")

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)


class CategoryDetailViewTests(WebTest):
    def test_list_active_products(self):
        _, root2 = CategoryFactory.create(name="Root 1"), CategoryFactory.create(
            name="Root 2"
        )
        child = CategoryFactory.create(parent=root2, name="Child 2")
        ProductFactory.create(categories=[child], active=True, name="active-visible")
        ProductFactory.create(
            categories=[child], active=False, name="inactive-not-visible"
        )

        category_page = self.app.get(child.get_absolute_url())

        self.assertContains(category_page, "active-visible")
        self.assertNotContains(category_page, "inactive-not-visible")


class ProductDetailViewTests(WebTest):
    def test_active_product(self):
        product = ProductFactory.create(
            active=True,
            with_image=True,
            name_nl="Testproduct",
            slug_nl="testproduct",
            name_en="Test product",
            slug_en="test-product",
        )

        with self.subTest("nl content"):
            with override("nl"):
                url = product.get_absolute_url()
            detail_page = self.app.get(
                url, extra_environ={"HTTP_ACCEPT_LANGUAGE": "nl"}
            )

            self.assertEqual(detail_page.status_code, 200)
            self.assertContains(detail_page, "Testproduct")

        with self.subTest("en content"):
            with override("en"):
                url = product.get_absolute_url()
            detail_page = self.app.get(
                url, extra_environ={"HTTP_ACCEPT_LANGUAGE": "en"}
            )

            self.assertEqual(detail_page.status_code, 200)
            self.assertContains(detail_page, "Test product")

    def test_inactive_product(self):
        product = ProductFactory.create(active=False)

        detail_page = self.app.get(product.get_absolute_url(), status=404)

        self.assertEqual(detail_page.status_code, 404)

    def test_category_expanded(self):
        root1, root2 = CategoryFactory.create(name="Root 1"), CategoryFactory.create(
            name="Root 2"
        )
        child1 = CategoryFactory.create(parent=root1, name="Child 1")
        child2 = CategoryFactory.create(parent=root2, name="Child 2")
        product = ProductFactory.create(categories=[child2])

        detail_page = self.app.get(product.get_absolute_url())

        self.assertEqual(detail_page.status_code, 200)
        visible_nodes = detail_page.pyquery(".tree-nav__item--show")
        self.assertEqual(len(visible_nodes), 2)
        node_labels = visible_nodes.map(lambda i, e: e.find("a").text.strip())
        self.assertEqual(node_labels, ["Root 2", "Child 2"])

    def test_default_category_expanded_with_multiple(self):
        root1, root2 = CategoryFactory.create(name="Root 1"), CategoryFactory.create(
            name="Root 2"
        )
        child1 = CategoryFactory.create(parent=root1, name="Child 1")
        child2 = CategoryFactory.create(parent=root2, name="Child 2")
        product = ProductFactory.create(categories=[child1, child2])

        detail_page = self.app.get(product.get_absolute_url())

        self.assertEqual(detail_page.status_code, 200)
        visible_nodes = detail_page.pyquery(".tree-nav__item--show")
        self.assertEqual(len(visible_nodes), 2)
        node_labels = visible_nodes.map(lambda i, e: e.find("a").text.strip())
        self.assertEqual(node_labels, ["Root 1", "Child 1"])

    def test_bad_referers_for_expanded_product_category(self):
        bad_category = CategoryFactory.build(slug="do-not-exist")
        category = CategoryFactory.create()
        product = ProductFactory.create(categories=[category])
        url = product.get_absolute_url()
        referers = (
            "",
            "https://example.com/external",
            "http://testserver/albums/",
            f"http://testserver/{uuid.uuid4()}",
            f"http://testserver{bad_category.get_absolute_url()}",
            f"http://testserver{url}",
        )

        for referer in referers:
            with self.subTest(referer=referer):

                detail_page = self.app.get(
                    url,
                    extra_environ={
                        "HTTP_REFERER": referer,
                    },
                )

                self.assertEqual(detail_page.status_code, 200)
                visible_nodes = detail_page.pyquery(".tree-nav__item--show")
                self.assertEqual(len(visible_nodes), 1)
                node_labels = visible_nodes.map(lambda i, e: e.find("a").text.strip())
                self.assertEqual(node_labels, [category.name])
