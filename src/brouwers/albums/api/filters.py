import rest_framework_filters as filters

from ..models import Photo


class PhotoFilter(filters.FilterSet):
    class Meta:
        model = Photo
        fields = ('album',)
