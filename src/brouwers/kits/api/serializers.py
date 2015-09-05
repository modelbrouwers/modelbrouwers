from rest_framework import serializers


from brouwers.utils.api.fields import ThumbnailField
from ..models import Brand, ModelKit, Scale


class BrandSerializer(serializers.ModelSerializer):

    logo = ThumbnailField((('small', '100x100'),), opts={'upscale': False}, required=False)

    class Meta:
        model = Brand
        fields = ('id', 'name', 'is_active', 'logo')


class ScaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scale
        fields = ('id', 'scale', '__unicode__')


class ModelKitSerializer(serializers.ModelSerializer):

    brand = BrandSerializer()
    scale = ScaleSerializer()
    box_image = ThumbnailField((('small', '600x400'),), opts={'upscale': False})

    class Meta:
        model = ModelKit
        fields = ('id', 'name', 'brand', 'scale', 'kit_number', 'box_image')


class CreateModelKitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelKit
        fields = ('id', 'name', 'brand', 'scale')
