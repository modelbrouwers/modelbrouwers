from datetime import date, timedelta

from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from brouwers.forum_tools.tests.factory_models import ForumCategoryFactory
from brouwers.users.tests.factories import UserFactory

from ..forms import GroupBuildForm
from ..models import GroupBuild, GroupbuildStatuses


class CreateTests(TestCase):  # TODO: conver to webtest
    def setUp(self):
        self.user = UserFactory.create()
        self.user2 = UserFactory.create()

        # mock request
        _request = HttpRequest()
        _request.user = self.user

        self.gb_data = {  # minimal data for form
            "theme": "Pokemon",
            "category": ForumCategoryFactory.create().id,
            "description": "Gotta catch 'em all!",
            "admins": [self.user.id, self.user2.id],
            "duration": 92,
        }
        self.create_form = GroupBuildForm(_request, data=self.gb_data)

    def test_created_concept_status(self):
        f = self.create_form
        self.assertTrue(f.is_valid())
        gb = f.save(commit=False)  # we're only interested in the instance
        self.assertEqual(gb.status, GroupbuildStatuses.concept)

    def test_create_only_authenticated_users(self):
        """Test that only authenticated users can submit concepts"""
        url = reverse("groupbuilds:create")
        next_url = settings.LOGIN_URL + "?next=" + url
        response = self.client.get(url)
        self.assertRedirects(response, next_url, status_code=302)

    def test_end_date_from_duration(self):
        """Test that the initial end date is set by the save method"""
        start = date(2014, 9, 16)
        end = start + timedelta(days=self.gb_data["duration"])

        fields = self.gb_data.copy()
        fields.update(
            {
                "category": ForumCategoryFactory.create(),
                "applicant_id": self.user.id,
            }
        )
        del fields["admins"]

        gb = GroupBuild.objects.create(start=start, **fields)
        self.assertEqual(gb.end, end)

    def test_submitter_is_admin(self):
        _request = HttpRequest()
        _request.user = self.user

        data = self.gb_data.copy()
        data["admins"] = [self.user2.id]  # not self.user

        f = GroupBuildForm(_request, data=data)
        self.assertTrue(f.is_valid())
        gb = f.save()
        gb = GroupBuild.objects.get(pk=gb.pk)
        self.assertIn(self.user, gb.admins.all())

    def test_applicant_set(self):
        f = self.create_form
        self.assertTrue(f.is_valid())
        gb = f.save(commit=False)
        self.assertEqual(gb.applicant, self.user)
