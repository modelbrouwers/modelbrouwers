import factory

from brouwers.users.tests.factories import UserFactory

from ..models import Build, BuildPhoto


class BuildFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: "Build {n}".format(n=n))

    class Meta:
        model = Build

    @factory.post_generation
    def kits(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            obj.kits.set(extracted)


class BuildPhotoFactory(factory.django.DjangoModelFactory):

    build = factory.SubFactory(BuildFactory)

    class Meta:
        model = BuildPhoto
