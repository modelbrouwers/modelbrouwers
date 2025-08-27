from django.test import TestCase
from django.test.utils import override_settings
from django.utils.http import urlencode

from brouwers.utils.tests import reload_urlconf

from .factories import ForumFactory, TopicFactory


@override_settings(PHPBB_URL="/forum/")
class URLTests(TestCase):
    def setUp(self):
        reload_urlconf()
        self.forum = ForumFactory()
        self.topic = TopicFactory(forum=self.forum)

    def test_absolute_url_forum(self):
        url = self.forum.get_absolute_url()
        expected_url = f"/forum/viewforum.php?f={self.forum.pk}"
        self.assertEqual(expected_url, url)

    def test_absolute_url_topic(self):
        url = self.topic.get_absolute_url()
        expected_qs = urlencode({"t": self.topic.pk})
        self.assertIn(expected_qs, url, "Missing topic id paramater")
        assert url.startswith("/forum/viewtopic.php?"), "Wrong url"
