from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from ..forms.fields import ForumIDField, TopicIDField
from ..models import Forum

from .custom_fields.models import MyModel
from .factory_models import ForumFactory, TopicFactory


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


class ModelFieldTests(TestCase):

    def setUp(self):
        self.forum = ForumFactory.create()
        self.topic1 = TopicFactory.create()
        self.topic2 = TopicFactory.create(forum=self.forum)

        max_forum = Forum.objects.values_list('pk', flat=True).order_by('-pk')[0]

        self.mm1 = MyModel.objects.create(forum_id=self.forum.pk, forum2_id=max_forum+1)
        # tests creation with nullable fields
        self.mm2 = MyModel.objects.create(forum_id=1, forum2_id=None)
        self.mm3 = MyModel.objects.create(forum_id=1)

    def test_creation(self):
        self.assertEqual(MyModel.objects.count(), 3)

    def test_getter(self):
        self.assertIsNotNone(self.mm1.forum_id)
        self.assertEqual(self.mm1.forum, self.forum)

        forums = Forum.objects.filter(pk=self.mm1.forum2_id).count()
        self.assertEqual(forums, 0)
        self.assertIsNone(self.mm1.forum2)

    def test_setter(self):
        self.assertIsNone(self.mm3.topic)

        self.mm3.topic = self.topic1
        self.assertEqual(self.mm3.topic_id, self.topic1.pk)
        self.mm3.save()

        mm3 = MyModel.objects.get(pk=self.mm3.pk)
        self.assertEqual(mm3.topic_id, self.topic1.pk)
        self.assertEqual(mm3.topic, self.topic1)

        mm3.topic = None
        mm3.save()
        self.assertNotEqual(mm3.topic_id, self.topic1.pk)
        self.assertIsNone(mm3.topic)

    def test_set_int(self):
        self.mm3.topic = 100
        self.mm3.save()
        self.assertEqual(self.mm3.topic_id, 100)
