from django.urls import reverse

from rest_framework.test import APITestCase

from .factories import GroupBuildFactory


class ApiTests(APITestCase):
    def test_groupbuild_detail(self):
        gb = GroupBuildFactory.create(
            theme="Testing the code",
            description="My groupbuild",
            rules="Newlined\nrules",
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
                "description": "My groupbuild",
                "rules": "Newlined\nrules",
                "start": gb.start,
                "end": gb.end,
                "status": gb.get_status_display(),
                "rules_topic": gb.rules_topic,
                "participants": [],
            },
        )
