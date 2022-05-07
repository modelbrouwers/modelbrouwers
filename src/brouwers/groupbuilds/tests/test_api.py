from django.urls import reverse

from rest_framework.test import APITestCase

from .factories import GroupBuildFactory


class ApiTests(APITestCase):
    def test_groupbuild_detail(self):
        gb = GroupBuildFactory.create(
            theme="Testing the code",
            description="[b]My BBCode[/b] groupbuild",
            rules="[i]BBCode[/i] rules",
        )

        endpoint = reverse("api:groupbuilds:groupbuild-detail", kwargs={"pk": gb.pk})
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(
            response.data,
            {
                "id": gb.id,
                "theme": "Testing the code",
                "url": gb.get_absolute_url(),
                "forum": gb.forum,
                "description": "<strong>My BBCode</strong> groupbuild",
                "rules": "<em>BBCode</em> rules",
                "start": gb.start,
                "end": gb.end,
                "status": gb.get_status_display(),
                "rules_topic": gb.rules_topic,
                "participants": [],
                "admins": [{"username": gb.applicant.username}],
            },
        )
