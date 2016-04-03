from django.core.exceptions import ValidationError
from django.test import TestCase

from brouwers.users.tests.factories import UserFactory
from ..models import KitReview, KitReviewVote, MIN_RATING, MAX_RATING
from .factories import KitReviewFactory, KitReviewVoteFactory


class KitReviewTest(TestCase):
    """
    Test the correct behaviour of brouwers.kitreviews.models.KitReview.
    """

    def test_kit_review_rating(self):
        kit_review1 = KitReviewFactory.create()
        self.assertEqual(kit_review1.rating, 50)

        kit_review2 = KitReviewFactory.create(rating=99)
        self.assertEqual(kit_review2.rating, 99)

        try:
            KitReviewFactory.create(rating='Good')
            self.fail('Should be impossible to add non-numeric values')
        except ValueError:
            pass

    def test_kit_review_validators(self):
        kit_review1 = KitReviewFactory.create(rating=1000)
        try:
            kit_review1.save()
            kit_review1.full_clean()
            self.fail('Should be impossible to add ratings greater than %d' % MAX_RATING)
        except ValidationError:
            pass

        kit_review2 = KitReviewFactory.create(rating=-5)
        try:
            kit_review2.save()
            kit_review2.full_clean()
            self.fail('Should be impossible to add ratings smaller than %d' % MIN_RATING)
        except ValidationError:
            pass
