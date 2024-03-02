from django.utils import timezone

import factory

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "User {0}".format(n))
    password = factory.django.Password("password")
    email = factory.Sequence(lambda n: "user-{0}@gmail.com".format(n))
    is_active = True
    last_login = timezone.now()

    class Meta:
        model = User
        skip_postgeneration_save = True

    class Params:
        superuser = factory.Trait(
            is_staff=True,
            is_superuser=True,
        )


class DataDownloadRequestFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "users.DataDownloadRequest"

    class Params:
        with_file = factory.Trait(
            zip_file=factory.django.FileField(data="foo", filename="some_file.zip"),
            finished=factory.LazyAttribute(lambda o: timezone.now()),
        )
