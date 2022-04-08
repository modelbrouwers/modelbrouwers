from rest_framework import permissions, viewsets

from ..models import Participant
from .serializers import ParticipantSerializer


class ParticipantIsSelf(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class ParticipantViewSet(viewsets.ModelViewSet):
    permission_classes = (ParticipantIsSelf,)
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
