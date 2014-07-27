from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from ..forms.fields import ForumIDField, TopicIDField


class FormFieldTests(SimpleTestCase):

    def setUp(self):
        self.data = {
            'forum_id': '10',
            'forum': 'http://www.example.com/forum/viewforum.php?f=32',
            'forum2': 'http://www.example.com/forum/viewforum.php?forum=32',
            'topic_id': '1',
            'topic': 'http://www.example.com/forum/viewforum.php?f=32&t=1',
            'topic2': 'http://www.example.com/forum/viewforum.php?f=32&topic=1',
        }
        self.forum_field = ForumIDField()
        self.topic_field = TopicIDField()
        self.invalid_url = 'http://example.com/'
        self.invalid_url2 = 'gibberish'

    def test_forum_field(self):

        value = self.forum_field.to_python(self.data['forum_id'])
        self.assertEqual(value, 10)

        value = self.forum_field.to_python(self.data['forum'])
        self.assertEqual(value, 32)

        forum_field2 = ForumIDField(urlparam='forum')
        value = forum_field2.to_python(self.data['forum2'])
        self.assertEqual(value, 32)

        with self.assertRaises(ValidationError):
            self.forum_field.to_python(self.invalid_url)

        with self.assertRaises(ValidationError):
            self.forum_field.to_python(self.invalid_url2)

    def test_topic_field(self):

        value = self.topic_field.to_python(self.data['topic_id'])
        self.assertEqual(value, 1)

        value = self.topic_field.to_python(self.data['topic'])
        self.assertEqual(value, 1)

        topic_field2 = TopicIDField(urlparam='topic')
        value = topic_field2.to_python(self.data['topic2'])
        self.assertEqual(value, 1)

        with self.assertRaises(ValidationError):
            self.topic_field.to_python(self.invalid_url)

        with self.assertRaises(ValidationError):
            self.topic_field.to_python(self.invalid_url2)

