from rest_framework import serializers

from brouwers.users.api.serializers import UserSerializer

from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'street', 'number', 'postal', 'city', 'country')
