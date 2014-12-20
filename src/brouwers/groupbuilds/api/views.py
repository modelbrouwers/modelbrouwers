from rest_framework import generics

from ..models import GroupBuild
from .serializers import GroupBuildSerializer


class GroupBuildDetail(generics.RetrieveAPIView):
    model = GroupBuild
    serializer_class = GroupBuildSerializer
