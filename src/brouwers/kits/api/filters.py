import rest_framework_filters as filters


from ..models import ModelKit, Brand


class ModelKitFilter(filters.FilterSet):

    name = filters.CharFilter(name='name', lookup_type='icontains')

    class Meta:
        model = ModelKit
        fields = ('brand', 'scale', 'name')


class BrandFilter(filters.FilterSet):

    name = filters.CharFilter(name='name', lookup_type='icontains')

    class Meta:
        model = Brand
        fields = ('name',)
