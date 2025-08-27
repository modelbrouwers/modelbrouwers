import factory

import brouwers.awards.models as models
from brouwers.users.tests.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class NominationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Nomination

    url = factory.Sequence(lambda n: f"http://foo-{n}.bar")
    name = factory.Sequence(lambda n: f"Project {n}")
    category = factory.SubFactory(CategoryFactory)
    brouwer = factory.Sequence(lambda n: f"brouwer-{n}")

    submitter = factory.SubFactory(UserFactory)
