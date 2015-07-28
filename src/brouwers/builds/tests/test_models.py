from django.test import TestCase

from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.forum_tools.tests.factories import TopicFactory
from .factories import BuildFactory


class BuildTests(TestCase):

    def setUp(self):
        self.kits = ModelKitFactory.create_batch(5)
        self.topic = TopicFactory.create()
        self.build = BuildFactory.create(kits=self.kits[:2], topic_id=self.topic.pk, topic_start_page=2)

    def test_topic_url(self):
        import bpdb; bpdb.set_trace()
