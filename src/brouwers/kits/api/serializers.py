from django.urls import reverse

from rest_framework import fields, serializers

from brouwers.utils.api.fields import ThumbnailField

from ..models import Boxart, Brand, ModelKit, Scale


class BrandSerializer(serializers.ModelSerializer):

    logo = ThumbnailField((('small', '100x100'),), opts={'upscale': False}, required=False)

    class Meta:
        model = Brand
        fields = ('id', 'name', 'is_active', 'logo')


class ScaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scale
        fields = ('id', 'scale', '__str__')


class ModelKitSerializer(serializers.ModelSerializer):

    brand = BrandSerializer()
    scale = ScaleSerializer()
    box_image = ThumbnailField((('small', '600x400'),), opts={'upscale': False, 'padding': True})

    class Meta:
        model = ModelKit
        fields = ('id', 'name', 'brand', 'scale', 'kit_number', 'difficulty', 'box_image')


def upload_exists(uuid):
    if not Boxart.objects.filter(uuid=uuid).exists():
        raise serializers.ValidationError('Invalid upload specified')


class CreateModelKitSerializer(serializers.ModelSerializer):

    box_image_uuid = fields.UUIDField(
        write_only=True, validators=[upload_exists],
        required=False, allow_null=True
    )

    url_kitreviews = fields.SerializerMethodField()

    class Meta:
        model = ModelKit
        fields = (
            'id', 'name', 'brand', 'scale', 'kit_number', 'difficulty',
            'url_kitreviews', 'box_image_uuid'
        )

    def get_url_kitreviews(self, obj):
        return reverse('kitreviews:review-add', kwargs={'slug': obj.slug})

    def create(self, validated_data):
        uuid = validated_data.pop('box_image_uuid', None)
        if uuid:
            boxart = Boxart.objects.get(uuid=uuid)
            validated_data['box_image'] = boxart.image
            boxart.delete()
        return super(CreateModelKitSerializer, self).create(validated_data)


class BoxartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Boxart
        fields = ('uuid', 'image')
