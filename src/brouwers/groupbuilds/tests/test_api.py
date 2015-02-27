from datetime import timedelta

from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework.test import APITestCase

from brouwers.forum_tools.tests.factory_models import ForumFactory, TopicFactory
from brouwers.users.tests.factories import UserFactory
from .factories import GroupBuildFactory, ParticipantFactory
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
            'admins': [{'username': gb.applicant.username}]
        })

    def test_participant_create(self):
        gb = GroupBuildFactory.create(status=GroupbuildStatuses.accepted)

        user = UserFactory.create()
        topic = TopicFactory.create(forum__forum_name=gb.theme,
                                    topic_title='Participant 1')

        endpoint = reverse('api:groupbuilds:groupbuild-participant',
                           kwargs={'pk': gb.pk})
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

    def test_gb_participant_check(self):
        """
        Test that the check returns the expected data.
        """
        user = UserFactory.create()
        self.client.login(username=user.username, password='password')
        forums = ForumFactory.create_batch(2)
        gb = GroupBuildFactory.create(status=GroupbuildStatuses.accepted,
                                      forum_id=forums[0].pk)

        five_min_ago = int((timezone.now() - timedelta(minutes=5)).strftime("%s"))
        topic1 = TopicFactory.create(forum=forums[0], create_time=five_min_ago)
        topic2 = TopicFactory.create(forum=forums[0])

        ParticipantFactory.create(
            groupbuild=gb, topic_id=topic1.pk, user=user)

        endpoint = reverse('api:groupbuilds:participant-check')

        invalid_data = {'forum_id': 'abcd', 'topic_id': topic1.pk}
        response = self.client.get(endpoint, invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.data, {'error': 'Bad query parameters'})

        # check with existing topic (created > 3 min ago)
        valid_data = {'forum_id': forums[0].pk, 'topic_id': topic1.pk}
        response = self.client.get(endpoint, valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'topic_created': False})

        # check with new topic
        valid_data['topic_id'] = topic2.pk
        response = self.client.get(endpoint, valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['topic_created'])
        self.assertEqual(response.data['groupbuild']['id'], gb.pk)

        # test irrelevant forum
        valid_data['forum_id'] = forums[1].pk
        response = self.client.get(endpoint, valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['topic_created'])
