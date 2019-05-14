from rest_framework import status, views
from rest_framework.response import Response

from ..models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileViewSet(views.APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user and not user.is_anonymous():
            u = UserProfile.objects.get(id=user.id)
            response = {'data': UserProfileSerializer(u).data}
            st = status.HTTP_200_OK
        else:
            response = {}
            st = status.HTTP_404_NOT_FOUND
        return Response(response, status=st)
