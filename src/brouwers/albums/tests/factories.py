import factory
import factory.fuzzy

from brouwers.users.tests.factories import UserFactory

from ..models import Album, AlbumGroup, Category, Photo

__all__ = ["CategoryFactory", "AlbumFactory", "PhotoFactory"]


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.fuzzy.FuzzyText()


class AlbumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Album

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    title = factory.Sequence(lambda n: "album {0}".format(n))


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo

    user = factory.SubFactory(UserFactory)
    album = factory.SubFactory(AlbumFactory)
    image = factory.django.ImageField()


class AlbumGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AlbumGroup
        skip_postgeneration_save = True

    album = factory.SubFactory(AlbumFactory)

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.users.set(extracted)
