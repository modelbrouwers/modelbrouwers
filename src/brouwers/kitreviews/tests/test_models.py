from django.core.exceptions import ValidationError
from django.test import TestCase

from brouwers.forum_tools.tests.factories import TopicFactory

from ..models import (
    DEFAULT_RATING, MAX_RATING, MIN_RATING, KitReview, KitReviewPropertyRating
)
from .factories import (
    KitReviewFactory, KitReviewPropertyFactory, KitReviewPropertyRatingFactory
)


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

    def test_annotate_mean_rating(self):
        review = KitReviewFactory.create()
        KitReviewPropertyRatingFactory.create_batch(3, kit_review=review, rating=75)

        # other ratings that would offset the average rating
        KitReviewPropertyRatingFactory.create_batch(3, rating=25)

        review = KitReview.objects.annotate_mean_rating().get(pk=review.pk)
        self.assertEqual(review.avg_rating, 75.0)  # and not 50
        self.assertEqual(review.rating_pct, 75.0)  # and not 50

        review2 = KitReviewFactory.create()
        KitReviewPropertyRatingFactory.create(kit_review=review2, rating=75)
        KitReviewPropertyRatingFactory.create(kit_review=review2, rating=25)

        review2 = KitReview.objects.annotate_mean_rating().get(pk=review2.pk)
        self.assertEqual(review2.avg_rating, 50.0)
        self.assertEqual(review2.rating_pct, 50.0)

    def test_topic_url(self):
        review = KitReviewFactory.build(topic_id=3141592)
        self.assertIsNone(review.topic_url)

        topic = TopicFactory.create()
        review2 = KitReviewFactory.build(topic_id=topic.pk)
        self.assertEqual(review2.topic_url, topic.get_absolute_url())

        review3 = KitReviewFactory.build(topic_id=topic.pk, external_topic_url='https://google.nl')
        self.assertEqual(review3.topic_url, topic.get_absolute_url())

        review4 = KitReviewFactory.build(external_topic_url='https://google.nl')
        self.assertEqual(review4.topic_url, 'https://google.nl')
