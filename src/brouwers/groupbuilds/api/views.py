from django.utils import timezone

from rest_framework import generics, views
from rest_framework.response import Response

from brouwers.forum_tools.models import Topic
from brouwers.forum_tools.api.serializers import TopicSerializer

from ..models import GroupBuild, Participant
from .serializers import GroupBuildSerializer
from .forms import TopicDetailsForm


class GroupBuildDetail(generics.RetrieveAPIView):
    model = GroupBuild
    serializer_class = GroupBuildSerializer


class GroupBuildParticipantCheckView(views.APIView):
    """
    View that checks if a topic belongs to a group build and was just created.
    """
    def get(self, request, *args, **kwargs):
        form = TopicDetailsForm(request.GET)
        if not form.is_valid():
            return Response({'error': 'Bad query parameters'})

        response = {}
        forum_id = form.cleaned_data['forum_id']
        # check if there's a groupbuild ongoing for this forum
        try:
            gb = GroupBuild.objects.get(forum=forum_id)
        except GroupBuild.DoesNotExist:
            pass

        topic_id = form.cleaned_data.get('topic_id')
        if topic_id:
            topic = Topic.objects.get(topic_id=topic_id)
            topic_created = (topic.created - timezone.now()).seconds < (3 * 60)
            response['topic_created'] = topic_created
            if topic_created:  # include gb and topic data
                response['groupbuild'] = GroupBuildSerializer(gb).data
                response['topic'] = TopicSerializer(topic).data

        return Response(response)
