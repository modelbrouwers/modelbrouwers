import factory

from ..models import ForumUser


class ForumUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ForumUser

    user_id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'User {n}'.format(n=n))
    username_clean = factory.PostGenerationMethodCall('_clean_username')
    user_email = factory.Sequence(lambda n: 'user{n}@domain.com'.format(n=n))
    user_email_hash = factory.PostGenerationMethodCall('get_email_hash')
    user_posts = 10
