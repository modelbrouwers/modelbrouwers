from django.utils import timezone

import factory

from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'User {0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email = factory.Sequence(lambda n: 'user-{0}@gmail.com'.format(n))
    is_active = True
    last_login = timezone.now()
