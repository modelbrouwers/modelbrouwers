from django.core.urlresolvers import reverse

from django_webtest import WebTest

from .factories import KitReviewFactory


class IndexViewTests(WebTest):

    def setUp(self):
        super(IndexViewTests, self).setUp()
        self.url = reverse('kitreviews:index')

    def test_index_shows_latest_reviews(self):
        """
        Assert that the index page shows the latest 5 reviews and (TODO) a form
        to search for a kit.
        """
        kitreviews = KitReviewFactory.create_batch(10)
        index = self.app.get(self.url)
        expected = [repr(review) for review in kitreviews[5:]]
        expected.reverse()
        self.assertQuerysetEqual(index.context['reviews'], expected)
