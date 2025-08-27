import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory

from ..models import Brand, ModelKit, Scale


class BrandFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Brand {n:05d}".format(n=n))
    logo = factory.django.ImageField()

    class Meta:
        model = Brand
        django_get_or_create = ("name",)


class ScaleFactory(factory.django.DjangoModelFactory):
    scale = factory.fuzzy.FuzzyInteger(16, 288)

    class Meta:
        model = Scale
        django_get_or_create = ("scale",)


class ModelKitFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Kit {n}".format(n=n))
    brand = factory.SubFactory(BrandFactory)
    scale = factory.SubFactory(ScaleFactory)
    box_image = factory.django.ImageField()
    submitter = factory.SubFactory(UserFactory)

    class Meta:
        model = ModelKit


class BoxartFactory(factory.django.DjangoModelFactory):
    image = factory.django.ImageField()

    class Meta:
        model = "kits.Boxart"
