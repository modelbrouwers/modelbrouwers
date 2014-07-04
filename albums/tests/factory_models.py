import factory

from users.tests.factory_models import UserFactory

from ..models import Album, Photo


class AlbumFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Album

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: 'album {0}'.format(n))


class PhotoFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Photo

    user = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)
