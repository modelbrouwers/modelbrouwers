import random

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django_webtest import WebTest

from brouwers.albums.tests.factories import AlbumFactory
from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin
from ..models import KitReview
from .factories import KitReviewFactory, KitReviewPropertyFactory


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


class AddReviewViewTests(LoginRequiredMixin, WebTest):
    """
    Tests for the 'add a kit review' page.
    """

    def setUp(self):
        super(AddReviewViewTests, self).setUp()
        self.url = reverse('kitreviews:add_review')

    def test_submit_review(self):
        """
        Asserts that submitting a review is only possible as logged in user.
        """
        # test that auth is required
        add_page = self.app.get(self.url)
        self._test_login_required(self.url, response=add_page)

        # add some test data - dummy albums etc.
        user = UserFactory.create()
        invalid_albums = AlbumFactory.create_batch(3)
        AlbumFactory.create_batch(4, user=user)
        kits = ModelKitFactory.create_batch(3)
        KitReviewPropertyFactory.create_batch(3)

        self.assertFalse(KitReview.objects.exists())
        add_page = self.app.get(self.url, user=user)
        form = add_page.form

        # try some invalid input
        form['model_kit'].select('')  # no kit submitted - a review must belong to a kit
        with self.assertRaises(ValueError):
            form['album'].select(str(random.choice(invalid_albums).pk))  # an album from a different user
        form['raw_text'] = ''  # empty review

        response = form.submit()
        self.assertFormError(response, 'form', 'raw_text', _('This field is required.'))
        self.assertFormError(response, 'form', 'model_kit', _('This field is required.'))

        # now select a kit
        kit = random.choice(kits)
        form['model_kit'].select(str(kit.pk))
        # and enter a review text
        form['raw_text'] = 'My very short review'

        response = form.submit()
        review = KitReview.objects.get()
        self.assertRedirects(response, review.get_absolute_url())
        self.assertEqual(review.ratings.count(), 3)
        self.assertEqual(review.model_kit, kit)
        self.assertEqual(review.raw_text, 'My very short review')
        self.assertEqual(review.reviewer, user)
