from django.test import SimpleTestCase

from ..widgets import ForumIDWidget, TopicIDWidget


class WidgetTests(SimpleTestCase):

    def setUp(self):
        self.data = {
            'forum_id': '10',
            'forum': 'http://www.example.com/forum/viewforum.php?f=32',
            'forum2': 'http://www.example.com/forum/viewforum.php?forum=32',
            'topic_id': '1',
            'topic': 'http://www.example.com/forum/viewforum.php?f=32&t=1',
            'topic2': 'http://www.example.com/forum/viewforum.php?f=32&topic=1',
        }

    def test_forum_widget(self):
        """
        Test that the forum id is correctly extracted from urls and that ID's
        are still accepted.
        """
        widget = ForumIDWidget()
        value = widget.value_from_datadict(self.data, None, 'forum_id')
        self.assertEqual(value, self.data['forum_id'])

        value2 = widget.value_from_datadict(self.data, None, 'forum')
        self.assertEqual(value2, '32')

    def test_forum_widget_urlparam(self):
        widget = ForumIDWidget(urlparam='forum')
        value = widget.value_from_datadict(self.data, None, 'forum2')
        self.assertEqual(value, '32')

    def test_topic_widget(self):
        widget = TopicIDWidget()
        value = widget.value_from_datadict(self.data, None, 'topic_id')
        self.assertEqual(value, self.data['topic_id'])

        value2 = widget.value_from_datadict(self.data, None, 'topic')
        self.assertEqual(value2, '1')

        widget2 = TopicIDWidget(urlparam='topic')
        value3 = widget2.value_from_datadict(self.data, None, 'topic2')
        self.assertEqual(value3, '1')
