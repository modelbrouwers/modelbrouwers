from django.core.exceptions import ValidationError
from django.test import TestCase

from brouwers.users.tests.factories import UserFactory
from ..models import KitReview, KitReviewVote, RATING_BASE
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

            # Todo Make these pass
            # try:
            #    KitReviewFactory.create(rating='1000')
            #    self.fail('Should be impossible to add ratings greater than RATING_BASE')
            # except ValueError:
            #   print('Test passed')
            # try:
            #    KitReviewFactory.create(rating='-5')
            #    self.fail('Should be impossible to add ratings less than zero')
            # except ValueError:
            #   print('Test passed')

    def test_kit_review_rating_scaled(self):
        kit_review1 = KitReviewFactory.create()
        self.assertEqual(kit_review1.rating_scaled, 2.5)

        kit_review2 = KitReviewFactory.create(rating=100)
        self.assertEqual(kit_review2.rating_scaled, 5)
