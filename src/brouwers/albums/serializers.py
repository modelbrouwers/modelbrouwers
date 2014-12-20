from rest_framework import serializers

from .models import Preferences


class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
