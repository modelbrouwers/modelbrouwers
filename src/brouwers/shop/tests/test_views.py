from django.urls import reverse
from django.utils.translation import ugettext as _

from django_webtest import WebTest

from .factories import ProductFactory
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin, WebTestFormMixin

from ..models import ProductReview


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
