from rest_framework import viewsets, permissions

from ..models import ModelKit, Brand, Scale
from .serializers import ModelKitSerializer, BrandSerializer, ScaleSerializer
from .filters import ModelKitFilter, BrandFilter, ScaleFilter


class ModelKitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelKit.objects.select_related('scale', 'brand')
    serializer_class = ModelKitSerializer
    filter_class = ModelKitFilter


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = BrandFilter
    pagination_class = None


class ScaleViewSet(viewsets.ModelViewSet):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = ScaleFilter
    pagination_class = None
