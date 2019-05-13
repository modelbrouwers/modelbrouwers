from rest_framework.response import Response
from rest_framework import views
from ..models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileViewSet(views.APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user

        if user:
            u = UserProfile.objects.get(id=user.id)
            response = {'data': UserProfileSerializer(u).data}

        else:
            response = {}
        return Response(response)
