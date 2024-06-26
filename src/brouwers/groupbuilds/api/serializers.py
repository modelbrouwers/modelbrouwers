from rest_framework import serializers

from brouwers.forum_tools.api.serializers import IDFieldSerializer

from ..models import GroupBuild, Participant


class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    topic = IDFieldSerializer()

    class Meta:
        model = Participant
        fields = ("id", "model_name", "username", "topic", "finished")


class GroupBuildSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="get_absolute_url", read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)
    description = serializers.CharField(read_only=True)
    rules = serializers.CharField(read_only=True)
    rules_topic = IDFieldSerializer()
    participants = ParticipantSerializer(many=True, source="participant_set")

    class Meta:
        model = GroupBuild
        fields = (
            "id",
            "theme",
            "url",
            "description",
            "start",
            "end",
            "status",
            "rules",
            "rules_topic",
            "participants",
        )
