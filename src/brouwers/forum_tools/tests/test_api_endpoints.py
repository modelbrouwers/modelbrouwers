from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .factories import TopicFactory


class TopicDetailEndpointTests(APITestCase):

    def test_anonymous_user(self):
        topic = TopicFactory.create()
        endpoint = reverse("api:forum_tools:topic-detail", kwargs={"pk": topic.pk})

        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
