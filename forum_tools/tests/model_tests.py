import urllib
import sys

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.importlib import import_module

from .factory_models import ForumFactory, TopicFactory


def reload_urlconf():
    if settings.ROOT_URLCONF in sys.modules:
        reload(sys.modules[settings.ROOT_URLCONF])
    return import_module(settings.ROOT_URLCONF)


@override_settings(PHPBB_URL='/forum/')
class URLTests(TestCase):
    def setUp(self):
        reload_urlconf()
        self.forum = ForumFactory()
        self.topic = TopicFactory(forum=self.forum)

    def test_absolute_url_forum(self):
        url = self.forum.get_absolute_url()
        expected_url = '/forum/viewforum.php?f={0}'.format(self.forum.pk)
        self.assertEquals(expected_url, url)

    def test_absolute_url_topic(self):
        url = self.topic.get_absolute_url()
        expected_qs = urllib.urlencode({'t': self.topic.pk})
        self.assertIn(expected_qs, url, 'Missing topic id paramater')
        assert url.startswith('/forum/viewtopic.php?'), 'Wrong url'
