import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory
from ..models import Brand, Scale, ModelKit


class BrandFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'Brand {n}'.format(n=n))
    logo = factory.django.ImageField()

    class Meta:
        model = Brand


class ScaleFactory(factory.django.DjangoModelFactory):

    scale = factory.fuzzy.FuzzyInteger(16, 288)

    class Meta:
        model = Scale


class ModelKitFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'Kit {n}'.format(n=n))
    brand = factory.SubFactory(BrandFactory)
    scale = factory.SubFactory(ScaleFactory)
    box_image = factory.django.ImageField()
    submitter = factory.SubFactory(UserFactory)

    class Meta:
        model = ModelKit
