from rest_framework import permissions, viewsets

from ..models import Brand, ModelKit, Scale
from .filters import BrandFilter, ModelKitFilter, ScaleFilter
from .serializers import (
    BrandSerializer, CreateModelKitSerializer, ModelKitSerializer,
    ScaleSerializer
)


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


# TODO: block 'update'
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = BrandFilter
    pagination_class = None


# TODO: block 'update'
class ScaleViewSet(viewsets.ModelViewSet):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = ScaleFilter
    pagination_class = None
