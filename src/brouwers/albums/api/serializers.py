from rest_framework import serializers

from brouwers.users.api.serializers import UserSerializer
from brouwers.utils.api.fields import ThumbnailField
from ..models import Photo
from ..serializers import PreferencesSerializer  # noqa


class UploadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('album', 'image', 'description')


class PhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = ThumbnailField(
        (('large', '1280'), ('thumb', '300x225')),  # large photo + actual thumb
        opts={'crop': 'center', 'upscale': False}
    )

    class Meta:
        model = Photo
        fields = ('id', 'user', 'description', 'image', 'width', 'height', 'uploaded', 'order')
