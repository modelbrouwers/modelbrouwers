from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView

from .serializers import UserWithProfileSerializer


class UserSelfView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserWithProfileSerializer

    def get_object(self):
        return self.request.user
