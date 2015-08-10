import rest_framework_filters as filters


from ..models import ModelKit


class ModelKitFilter(filters.FilterSet):
    class Meta:
        model = ModelKit
        fields = ('brand', 'scale')
