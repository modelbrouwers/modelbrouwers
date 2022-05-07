from rest_framework import serializers

from brouwers.general.models import UserProfile

from ..models import User


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance != self.context["request"].user:
            raise RuntimeError(
                "You are (inadvertedly) leaking sensitive data to other users!"
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
