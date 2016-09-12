from django.core.urlresolvers import reverse

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
        fields = ('id', 'scale', '__unicode__')


class ModelKitSerializer(serializers.ModelSerializer):

    brand = BrandSerializer()
    scale = ScaleSerializer()
    box_image = ThumbnailField((('small', '600x400'),), opts={'upscale': False, 'padding': True})

    class Meta:
        model = ModelKit
        fields = ('id', 'name', 'brand', 'scale', 'kit_number', 'difficulty', 'box_image')


class CreateModelKitSerializer(serializers.ModelSerializer):

    url_kitreviews = fields.SerializerMethodField()

    class Meta:
        model = ModelKit
        fields = ('id', 'name', 'brand', 'scale', 'kit_number', 'difficulty', 'url_kitreviews')

    def get_url_kitreviews(self, obj):
        return reverse('kitreviews:review-add', kwargs={'slug': obj.slug})


class BoxartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Boxart
        fields = ('uuid', 'image')
