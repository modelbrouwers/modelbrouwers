from rest_framework import viewsets, permissions

from ..models import ModelKit, Brand, Scale
from .serializers import CreateModelKitSerializer, ModelKitSerializer, BrandSerializer, ScaleSerializer
from .filters import ModelKitFilter, BrandFilter, ScaleFilter


class ModelKitViewSet(viewsets.ModelViewSet):
    queryset = ModelKit.objects.select_related('scale', 'brand')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ModelKitSerializer
    filter_class = ModelKitFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateModelKitSerializer
        return super(ModelKitViewSet, self).get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)


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
