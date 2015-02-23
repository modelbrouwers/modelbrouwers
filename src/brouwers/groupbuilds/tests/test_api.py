from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase

from brouwers.forum_tools.tests.factory_models import TopicFactory
from brouwers.users.tests.factories import UserFactory
from .factories import GroupBuildFactory
from ..models import GroupbuildStatuses


class ApiTests(APITestCase):

    def test_groupbuild_detail(self):
        gb = GroupBuildFactory.create(
            theme='Testing the code',
            description='[b]My BBCode[/b] groupbuild',
            rules='[i]BBCode[/i] rules'
        )

        endpoint = reverse('api:groupbuilds:groupbuild-detail', kwargs={'pk': gb.pk})
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(response.data, {
            'id': gb.id,
            'theme': 'Testing the code',
            'url': gb.get_absolute_url(),
            'forum': gb.forum,
            'description': '<strong>My BBCode</strong> groupbuild',
            'rules': '<em>BBCode</em> rules',
            'start': gb.start,
            'end': gb.end,
            'status': gb.get_status_display(),
            'rules_topic': gb.rules_topic,
            'participants': [],
            'admins': []
        })

    def test_participant_create(self):
        gb = GroupBuildFactory.create(status=GroupbuildStatuses.accepted)

        user = UserFactory.create()
        topic = TopicFactory.create(forum__forum_name=gb.theme, topic_title='Participant 1')

        endpoint = reverse('api:groupbuilds:groupbuild-participant', kwargs={'pk': gb.pk})
        data = {
            'groupbuild': gb.pk,
            'model_name': 'Participant 1',
            'topic': topic.pk,
        }
        self.client.login(username=user.username, password='password')
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, 201)  # created

        self.assertEqual(gb.participant_set.count(), 1)
        participant = gb.participant_set.first()
        self.assertEqual(participant.topic_id, topic.topic_id)
        self.assertEqual(participant.model_name, 'Participant 1')
