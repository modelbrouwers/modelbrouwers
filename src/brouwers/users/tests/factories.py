import functools

from django.contrib.auth.models import Permission
from django.utils import timezone

import factory

from ..models import User


@functools.lru_cache
def get_all_permissions():
    all_permissions = Permission.objects.prefetch_related("content_type")
    mapped_perms = {
        f"{perm.content_type.app_label}.{perm.codename}": perm
        for perm in all_permissions
    }
    return mapped_perms


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"User {n}")
    password = factory.django.Password("password")
    email = factory.Sequence(lambda n: f"user-{n}@gmail.com")
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

    @factory.post_generation
    def permissions(obj, create, extracted, **kwargs):
        """ """
        if not create or not extracted:
            return

        perms = get_all_permissions()
        expected_perms = [perms[code] for code in extracted]
        obj.user_permissions.set(expected_perms)
        return expected_perms


class DataDownloadRequestFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "users.DataDownloadRequest"

    class Params:
        with_file = factory.Trait(
            zip_file=factory.django.FileField(data="foo", filename="some_file.zip"),
            finished=factory.LazyAttribute(lambda o: timezone.now()),
        )
