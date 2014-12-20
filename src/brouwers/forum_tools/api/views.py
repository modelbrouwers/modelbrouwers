from rest_framework import generics

from ..models import Forum, Topic
from .serializers import ForumSerializer, TopicSerializer


class ForumDetail(generics.RetrieveAPIView):
    model = Forum
    serializer_class = ForumSerializer


class TopicDetail(generics.RetrieveAPIView):
    model = Topic
    serializer_class = TopicSerializer
