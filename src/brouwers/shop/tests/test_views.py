from django.template import engines
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import ugettext as _

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ..models import Category
from .factories import CartFactory


class BreadcrumbsTests(TestCase):
    def _load_template(self, tpl):
        return engines["django"].from_string(tpl)

    def test_breadcrumbs_render(self):
        """
        Asserts that breadcrumbs are rendered correctly.
        """
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
            '<a class="breadcrumbs__item" href="/winkel/categories/root/">Root</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/child1/">Child1</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/child2/">Child2</a></div>',
        )

        rendered2 = template.render({"node": child1})
        self.assertHTMLEqual(
            rendered2,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/root/">Root</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/child1/">Child1</a>',
        )

        rendered3 = template.render({"node": root})
        self.assertHTMLEqual(
            rendered3,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/root/">Root</a>',
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
