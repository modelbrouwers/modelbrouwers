import factory

from forum_tools.tests.factory_models import ForumCategoryFactory
from users.tests.factory_models import UserFactory

from ..models import GroupBuild


class GroupBuildFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = GroupBuild

    theme = factory.Sequence(lambda n: "Groupbuild {0}".format(n))
    category = factory.SubFactory(ForumCategoryFactory)
    description = 'Groupbuild with [b]BBCode[/b]'
    rules = 'Groupbuild rules with [i]BBCode[/i]'
    applicant = UserFactory()
    reason_denied = 'Denied: [quote="admin"]BBCode[/quote]'
