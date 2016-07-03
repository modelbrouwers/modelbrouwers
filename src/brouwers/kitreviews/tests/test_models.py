from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import KitReviewPropertyRating, MIN_RATING, MAX_RATING, DEFAULT_RATING
from .factories import KitReviewFactory, KitReviewPropertyFactory, KitReviewPropertyRatingFactory


class KitReviewPropertyRatingTest(TestCase):
    """ Test the correct behaviour of brouwers.kitreviews.models.KitReviewPropertyRating. """

    def setUp(self):
        self.kit_review = KitReviewFactory.create()
        self.prop = KitReviewPropertyFactory.create()

    def test_kit_review_property_rating(self):
        # Test default rating
        kit_review_property_rating1 = KitReviewPropertyRating.objects.create(kit_review=self.kit_review,
                                                                             prop=self.prop)
        self.assertEqual(kit_review_property_rating1.rating, DEFAULT_RATING)

        # Test that it's impossible to assign values less than MIN_RATING to review prop rating
        kit_review_property_rating2 = KitReviewPropertyRatingFactory.create(rating=MIN_RATING - 1)
        with self.assertRaises(ValidationError):
            kit_review_property_rating2.full_clean()

        # Test that it's impossible to assign values larger than MAX_RATING to review prop rating
        kit_review_property_rating3 = KitReviewPropertyRatingFactory.create(rating=MAX_RATING + 10)
        with self.assertRaises(ValidationError):
            kit_review_property_rating3.full_clean()

        # Test that it's impossible to assign non-numeric values to review prop rating
        with self.assertRaises(ValueError):
            KitReviewPropertyRatingFactory.create(rating='good')


class KitReviewTests(TestCase):

    """
    Unit tests on the KitReview model
    """

    def test_reviewer_name(self):
        review1 = KitReviewFactory.build(
            reviewer__first_name='John',
            reviewer__last_name='Doe',
            show_real_name=True,
        )
        self.assertEqual(review1.reviewer_name, review1.reviewer.get_full_name())

        review2 = KitReviewFactory.build(
            reviewer__first_name='John',
            reviewer__last_name='Doe',
            show_real_name=False,
        )
        self.assertEqual(review2.reviewer_name, review2.reviewer.username)
