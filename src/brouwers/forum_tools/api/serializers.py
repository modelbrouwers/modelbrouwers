import HTMLParser

from rest_framework import serializers
from rest_framework import fields

from ..models import Forum, Topic

html_parser = HTMLParser.HTMLParser()


class IDFieldSerializer(serializers.Serializer):
    title = fields.SerializerMethodField('obj_title')
    url = fields.URLField(source='get_absolute_url', read_only=True)

    def obj_title(self, obj):
        return html_parser.unescape(unicode(obj))


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    is_dead = fields.BooleanField(read_only=True)
    age = fields.CharField(read_only=True)
    text_dead = fields.CharField(read_only=True)
    topic_title = fields.SerializerMethodField('obj_topic_title')

    class Meta:
        model = Topic
        fields = '__all__'

    def obj_topic_title(self, obj):
        return html_parser.unescape(obj.topic_title)
