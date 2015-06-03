import factory
import factory.fuzzy

from brouwers.users.tests.factory_models import UserFactory
from ..models import Album, Photo, Category


__all__ = ['CategoryFactory', 'AlbumFactory', 'PhotoFactory']


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.fuzzy.FuzzyText()


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    title = factory.Sequence(lambda n: 'album {0}'.format(n))


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    user = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)
    image = factory.django.ImageField()
