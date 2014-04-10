from django.contrib.auth import get_user_model

import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user_{n}'.format(n=n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_active = True
