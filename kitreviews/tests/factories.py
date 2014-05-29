import factory

from ..models import Brand


class BrandFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Brand

    name = factory.Sequence(lambda n: 'Brand {0}'.format(n))
