from django.db import IntegrityError
from django.test import TestCase, override_settings

from brouwers.forum_tools.tests.factories import TopicFactory
from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.utils.tests import reload_urlconf

from .factories import BuildFactory


@override_settings(PHPBB_URL='/forum', PHPBB_POSTS_PER_PAGE=5)
class BuildTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BuildTests, cls).setUpClass()
        reload_urlconf()

    def setUp(self):
        self.kits = ModelKitFactory.create_batch(5)
        self.topic = TopicFactory.create()
        self.build = BuildFactory.create(kits=self.kits[:2], topic_id=self.topic.pk, topic_start_page=2)

    def test_topic_url(self):
        self.assertEqual(
            self.build.topic_url,
            '/forum/viewtopic.php?t={0}&f={1}&start=5'.format(self.topic.pk, self.topic.forum_id)
        )

    def test_topic_url_no_startpage(self):
        topic = TopicFactory.create()
        build = BuildFactory.create(topic_id=topic.pk)
        self.assertEqual(
            build.topic_url,
            '/forum/viewtopic.php?t={0}&f={1}'.format(topic.pk, topic.forum_id)
        )

    def test_topic_url_None(self):
        build = BuildFactory.create()
        self.assertIsNone(build.topic)
        self.assertIsNone(build.topic_url)

    def test_topic_unique(self):
        with self.assertRaises(IntegrityError):
            BuildFactory.create(topic_id=self.topic.pk)
