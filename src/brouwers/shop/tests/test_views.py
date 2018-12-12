from django.urls import reverse
from django.utils.translation import ugettext as _
from django.template import engines
from django.test import TestCase
from django_webtest import WebTest

from .factories import ProductFactory
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin, WebTestFormMixin

from ..models import ProductReview
from .factories import CategoryFactory


class AddReviewViewTests(WebTestFormMixin, LoginRequiredMixin, WebTest):
    """
    Tests for the product review form.
    """

    def setUp(self):
        super(AddReviewViewTests, self).setUp()
        self.product = ProductFactory.create()
        self.url = reverse('shop:product-detail', kwargs={'slug': self.product.slug})

    def test_submit_review(self):
        """
        Asserts that submitting a review is only possible as logged in user.
        """
        # test that auth is required to see the form
        product_page = self.app.get(self.url)
        with self.assertRaises(TypeError):
            form = product_page.form

        user = UserFactory.create()
        product_page = self.app.get(self.url, user=user)
        form = product_page.form

        # try some invalid input
        form['text'] = ''  # empty review

        response = form.submit()
        self.assertFormError(response, 'form', 'text', _('This field is required.'))
        self.assertFormError(response, 'form', 'rating', _('This field is required.'))

        # and enter a review text
        form['text'] = 'My very short review'
        form['rating'] = '1'

        response = form.submit()
        review = ProductReview.objects.get()
        self.assertRedirects(response, self.product.get_absolute_url())
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.text, 'My very short review')
        self.assertEqual(review.reviewer, user)


class BreadcrumbsTests(TestCase):

    def _load_template(self, tpl):
        return engines['django'].from_string(tpl)

    def test_breadcrumbs_render(self):
        """
        Asserts that breadcrumbs are rendered correctly.
        """
        tpl = "{% include 'shop/includes/breadcrumbs.html' with curr_node=node%}"
        template = self._load_template(tpl)

        root = CategoryFactory.create().add_root(name='Root')
        child1 = root.add_child(name='Child1')
        child2 = child1.add_child(name='Child2')

        rendered = template.render({'node': child2})
        self.assertHTMLEqual(
            rendered,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/root/">Root</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/child1/">Child1</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/child2/">Child2</a></div>'
        )

        rendered2 = template.render({'node': child1})
        self.assertHTMLEqual(
            rendered2,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/root/">Root</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/child1/">Child1</a>'
        )

        rendered3 = template.render({'node': root})
        self.assertHTMLEqual(
            rendered3,
            '<div class="breadcrumbs">'
            '<a class="breadcrumbs__item" href="/winkel/">Home</a>'
            '<span class="breadcrumbs__separator"> > </span>'
            '<a class="breadcrumbs__item" href="/winkel/categories/root/">Root</a>'
        )
