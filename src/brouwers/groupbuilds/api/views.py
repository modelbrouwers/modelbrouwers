import HTMLParser

from django.utils import timezone

import Levenshtein
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from brouwers.forum_tools.api.serializers import TopicSerializer
from brouwers.forum_tools.models import Topic

from ..models import GroupBuild, Participant
from .forms import TopicDetailsForm
from .serializers import (
    GroupBuildSerializer, ParticipantCreateSerializer, ParticipantSerializer
)

html_parser = HTMLParser.HTMLParser()


class GroupBuildDetail(generics.RetrieveAPIView):
    queryset = GroupBuild.objects.all()
    serializer_class = GroupBuildSerializer


class GroupBuildParticipantCheckView(views.APIView):
    """
    View that checks if a topic belongs to a group build and was just created.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        form = TopicDetailsForm(request.GET)
        if not form.is_valid():
            return Response({'error': 'Bad query parameters'},
                            status=status.HTTP_400_BAD_REQUEST)

        response = {}
        forum_id = form.cleaned_data['forum_id']
        # check if there's a groupbuild ongoing for this forum
        try:
            gb = GroupBuild.objects.get(forum=forum_id)
        except GroupBuild.DoesNotExist:
            gb = None

        topic = Topic.objects.filter(**form.cleaned_data).first()
        topic_created = (
            topic is not None and
            (timezone.now() - topic.created).seconds < (3 * 60)
        )

        response['topic_created'] = topic_created
        if topic_created and gb is not None:  # include gb and topic data
            participants = Participant.objects.filter(user=request.user, groupbuild=gb, topic_id=None)
            matches = []
            topic_title = html_parser.unescape(topic.topic_title).lower()
            for participant in participants:
                ratio = Levenshtein.ratio(participant.model_name.lower(), topic_title)
                if ratio > 0.25:
                    matches.append((participant, ratio))
            matches = sorted(matches, key=lambda x: x[1])
            if matches:
                response['participant'] = ParticipantSerializer(matches[-1][0]).data
            response['groupbuild'] = GroupBuildSerializer(gb).data
            response['topic'] = TopicSerializer(topic).data

        return Response(response)


class ParticipantCreateView(generics.CreateAPIView):
    model = Participant
    serializer_class = ParticipantCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
