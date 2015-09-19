from rest_framework import generics

from ..models import Forum, Topic
from .serializers import ForumSerializer, TopicSerializer


class ForumDetail(generics.RetrieveAPIView):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer


class TopicDetail(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
