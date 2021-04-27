import rest_framework_filters as filters

from ..models import Brand, ModelKit, Scale


class ModelKitFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ModelKit
        fields = ("brand", "scale", "name")


class BrandFilter(filters.FilterSet):

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Brand
        fields = ("name",)


class ScaleFilter(filters.FilterSet):

    scale = filters.NumberFilter(field_name="scale")

    class Meta:
        model = Scale
        fields = ("scale",)
