from rest_framework import serializers
from rest_framework import fields


class IDFieldSerializer(serializers.Serializer):
    title = fields.CharField(source='__unicode__', read_only=True)
    url = fields.URLField(source='get_absolute_url', read_only=True)
