import html

from django.contrib.auth.models import AnonymousUser

from rest_framework import fields, serializers

from brouwers.users.models import User

from ..models import Forum, Topic


class IDFieldSerializer(serializers.Serializer):
    title = fields.SerializerMethodField("obj_title")
    url = fields.URLField(source="get_absolute_url", read_only=True)

    def obj_title(self, obj):
        return html.unescape(str(obj))


class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    is_dead = fields.SerializerMethodField(read_only=True)
    age = fields.CharField(read_only=True)
    text_dead = fields.CharField(read_only=True)
    topic_title = fields.SerializerMethodField("obj_topic_title")

    class Meta:
        model = Topic
        fields = "__all__"

    def obj_topic_title(self, obj):
        return html.unescape(obj.topic_title)

    def get_is_dead(self, obj) -> bool:
        user: User | AnonymousUser = self.context["request"].user
        match user:
            case User() if obj.author_id == user.forumuser_id:
                return False
            case _:
                return obj.is_dead
