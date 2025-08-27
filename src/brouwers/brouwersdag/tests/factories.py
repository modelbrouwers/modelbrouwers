import factory

from brouwers.kits.tests.factories import BrandFactory

from ..models import Competition, ShowCasedModel


class CompetitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Competition

    name = factory.Sequence(lambda n: f"Competition {n}")
    is_current = False


class ShowCasedModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShowCasedModel

    owner_name = factory.Sequence(lambda n: f"Owner {n}")
    email = factory.Sequence(lambda n: f"Owner {n}")
    name = factory.Sequence(lambda n: f"Model {n}")
    brand = factory.SubFactory(BrandFactory)
    scale = 48
