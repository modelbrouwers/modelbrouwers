from rest_framework import serializers

from brouwers.general.models import UserProfile

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "street",
            "number",
            "postal",
            "city",
            "country",
        )


class UserWithProfileSerializer(UserSerializer):
    profile = UserProfileSerializer()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("profile",)
