from rest_framework import generics

from brouwers.general.models import Announcement

from ..models import Forum, Topic
from .serializers import AnnouncementSerializer, ForumSerializer, TopicSerializer


class ForumDetail(generics.RetrieveAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


class TopicDetail(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class AnnouncementView(generics.RetrieveAPIView):
    queryset = Announcement.objects.none()
    serializer_class = AnnouncementSerializer

    def get_object(self):
        return Announcement.objects.get_current() or Announcement(text=None)
