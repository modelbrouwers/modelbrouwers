import factory

from brouwers.kitreviews.tests.factories import BrandFactory

from ..models import Competition, ShowCasedModel


class CompetitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Competition

    name = factory.Sequence(lambda n: 'Competition {0}'.format(n))
    is_current = False


class ShowCasedModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShowCasedModel

    owner_name = factory.Sequence(lambda n: 'Owner {0}'.format(n))
    email = factory.Sequence(lambda n: 'Owner {0}'.format(n))
    name = factory.Sequence(lambda n: 'Model {0}'.format(n))
    brand = factory.SubFactory(BrandFactory)
    scale = 48
