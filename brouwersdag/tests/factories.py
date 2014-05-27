import factory

from ..models import Competition


class CompetitionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Competition

    name = factory.Sequence(lambda n: 'Competition {0}'.format(n))
    is_current = False
