from django.utils import timezone

from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from brouwers.forum_tools.models import Topic
from brouwers.forum_tools.api.serializers import TopicSerializer

from ..models import GroupBuild, Participant
from .serializers import GroupBuildSerializer, ParticipantCreateSerializer
from .forms import TopicDetailsForm


class GroupBuildDetail(generics.RetrieveAPIView):
    model = GroupBuild
    serializer_class = GroupBuildSerializer


class GroupBuildParticipantCheckView(views.APIView):
    """
    View that checks if a topic belongs to a group build and was just created.
    """
    permission_classes = (IsAuthenticated,)

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
            gb = None

        topic_id = form.cleaned_data.get('topic_id')
        if topic_id:
            topic = Topic.objects.get(topic_id=topic_id)
            topic_created = (timezone.now() - topic.created).seconds < (3 * 60)
            response['topic_created'] = topic_created
            if topic_created and gb is not None:  # include gb and topic data
                response['groupbuild'] = GroupBuildSerializer(gb).data
                response['topic'] = TopicSerializer(topic).data

        return Response(response)


class ParticipantListCreateView(generics.ListCreateAPIView):
    model = Participant
    serializer_class = ParticipantCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(ParticipantListCreateView, self).get_queryset()
        return qs.filter(groupbuild_id=self.kwargs['pk'])

    def pre_save(self, obj):
        super(ParticipantListCreateView, self).pre_save(obj)
        obj.user = self.request.user
