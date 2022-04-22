import factory

import brouwers.awards.models as models
from brouwers.users.tests.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: "Category {0}".format(n))
    slug = factory.Sequence(lambda n: "category-{0}".format(n))


class NominationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Nomination

    url = factory.Sequence(lambda n: "http://foo-{0}.bar".format(n))
    name = factory.Sequence(lambda n: "Project {0}".format(n))
    category = factory.SubFactory(CategoryFactory)
    brouwer = factory.Sequence(lambda n: "brouwer-{0}".format(n))

    submitter = factory.SubFactory(UserFactory)
