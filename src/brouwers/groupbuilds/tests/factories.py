import factory

from brouwers.forum_tools.tests.factory_models import ForumCategoryFactory
from brouwers.users.tests.factories import UserFactory

from ..models import GroupBuild, Participant


class GroupBuildFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GroupBuild

    theme = factory.Sequence(lambda n: "Groupbuild {0}".format(n))
    category = factory.SubFactory(ForumCategoryFactory)
    description = "Groupbuild with [b]BBCode[/b]"
    rules = "Groupbuild rules with [i]BBCode[/i]"
    applicant = factory.SubFactory(UserFactory)
    reason_denied = 'Denied: [quote="admin"]BBCode[/quote]'


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant

    groupbuild = factory.SubFactory(GroupBuildFactory)
    user = factory.SubFactory(UserFactory)
    model_name = factory.Sequence(lambda n: "Participant {0}".format(n))
