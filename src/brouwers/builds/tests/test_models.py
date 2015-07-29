from django.test import TestCase, override_settings
from django.db import IntegrityError

from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.forum_tools.tests.factories import TopicFactory
from .factories import BuildFactory


@override_settings(PHPBB_URL='/forum', PHPBB_POSTS_PER_PAGE=5)
class BuildTests(TestCase):

    def setUp(self):
        self.kits = ModelKitFactory.create_batch(5)
        self.topic = TopicFactory.create()
        self.build = BuildFactory.create(kits=self.kits[:2], topic_id=self.topic.pk, topic_start_page=2)

    def test_topic_url(self):
        self.assertEqual(
            self.build.topic_url,
            '/forum/viewtopic.php?t=1&f=1&start=5'
        )

    def test_topic_unique(self):
        with self.assertRaises(IntegrityError):
            BuildFactory.create(topic_id=self.topic.pk)
