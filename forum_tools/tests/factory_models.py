import factory

from ..models import ForumUser


def create_from_user(user):
    forum_user = ForumUserFactory(
        username=user.username,
        user_email=user.email,
    )
    user.forumuser_id = forum_user.user_id
    user.save()
    user.forumuser = forum_user
    return forum_user


class ForumUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ForumUser

    user_id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'User {n}'.format(n=n))
    username_clean = factory.PostGenerationMethodCall('_clean_username')
    user_email = factory.Sequence(lambda n: 'user{n}@domain.com'.format(n=n))
    user_email_hash = factory.PostGenerationMethodCall('get_email_hash')
    user_posts = 10
