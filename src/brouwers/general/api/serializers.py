from rest_framework import serializers

from brouwers.users.api.serializers import UserSerializer
from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        user = UserSerializer
        fields = ('user', 'street', 'number', 'postal', 'city', 'country')
