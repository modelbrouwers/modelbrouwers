from django.test import TestCase

from forum_tools.tests.factory_models import ForumCategoryFactory
from users.tests.factory_models import UserFactory

from ..forms import GroupBuildForm
from ..models import GroupbuildStatuses


class CreateTests(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()

        self.gb_data = { # minimal data
            'theme': 'Pokemon',
            'category': ForumCategoryFactory().id,
            'description': 'Gotta catch \'em all!',
            'admins': [self.user.id, self.user2.id],
            'duration': 92,
        }
        self.create_form = GroupBuildForm(data=self.gb_data)

    def test_created_concept_status(self):
        f = self.create_form
        self.assertTrue(f.is_valid())
        gb = f.save(commit=False) # we're only interested in the instance
        self.assertEqual(gb.status, GroupbuildStatuses.concept)

    def test_create_only_authenticated_users(self):
        pass

    def test_end_date_from_duration(self):
        pass

    def test_submitter_is_admin(self):
        pass

    def test_applicant_set(self):
        pass
