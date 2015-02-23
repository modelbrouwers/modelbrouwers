import time

import factory

from ..models import ForumUser, ForumCategory, Forum, Topic


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


class ForumCategoryFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ForumCategory

    name = factory.Sequence(lambda n: 'Category {0}'.format(n))


class ForumFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Forum

    forum_id = factory.Sequence(lambda n: n)
    forum_name = factory.Sequence(lambda n: 'Forum {0}'.format(n))


class TopicFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Topic

    topic_id = factory.Sequence(lambda n: n)
    forum = factory.SubFactory(ForumFactory)
    topic_title = factory.Sequence(lambda n: 'Topic {0}'.format(n))
    create_time = factory.LazyAttribute(lambda *args: int(time.time()))
