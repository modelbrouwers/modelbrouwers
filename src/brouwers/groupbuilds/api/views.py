from rest_framework import generics

from ..models import GroupBuild
from .serializers import GroupBuildSerializer


class GroupBuildDetail(generics.RetrieveAPIView):
    queryset = GroupBuild.objects.all()
    serializer_class = GroupBuildSerializer
