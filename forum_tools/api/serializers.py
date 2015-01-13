from rest_framework import serializers
from rest_framework import fields

from ..models import Forum, Topic


class IDFieldSerializer(serializers.Serializer):
    title = fields.CharField(source='__unicode__', read_only=True)
    url = fields.URLField(source='get_absolute_url', read_only=True)


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
