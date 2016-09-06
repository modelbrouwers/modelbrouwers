import factory

from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.users.tests.factories import UserFactory

from ..models import (
    KitReview, KitReviewProperty, KitReviewPropertyRating, KitReviewVote
)


class KitReviewFactory(factory.django.DjangoModelFactory):
    model_kit = factory.SubFactory(ModelKitFactory)
    raw_text = factory.Faker('text')
    submitted_on = factory.Faker('date')

    reviewer = factory.SubFactory(UserFactory)

    class Meta:
        model = KitReview


class KitReviewVoteFactory(factory.django.DjangoModelFactory):
    review = factory.SubFactory(KitReviewFactory)
    voter = factory.SubFactory(UserFactory)

    class Meta:
        model = KitReviewVote


class KitReviewPropertyFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('text')

    class Meta:
        model = KitReviewProperty


class KitReviewPropertyRatingFactory(factory.django.DjangoModelFactory):
    kit_review = factory.SubFactory(KitReviewFactory)
    prop = factory.SubFactory(KitReviewPropertyFactory)

    class Meta:
        model = KitReviewPropertyRating
