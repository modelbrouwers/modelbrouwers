from django.utils import timezone

from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from brouwers.forum_tools.models import Topic
from brouwers.forum_tools.api.serializers import TopicSerializer

from ..models import GroupBuild, Participant
from .serializers import GroupBuildSerializer, ParticipantCreateSerializer
from .forms import TopicDetailsForm


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
            response['groupbuild'] = GroupBuildSerializer(gb).data
            response['topic'] = TopicSerializer(topic).data

        return Response(response)


class ParticipantCreateView(generics.CreateAPIView):
    model = Participant
    serializer_class = ParticipantCreateSerializer
    permission_classes = (IsAuthenticated,)

    def pre_save(self, obj):
        super(ParticipantCreateView, self).pre_save(obj)
        obj.user = self.request.user
