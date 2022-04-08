from rest_framework import mixins, parsers, permissions, viewsets
from rest_framework.settings import api_settings

from ..models import Boxart, Brand, ModelKit, Scale
from .filters import BrandFilter, ModelKitFilter, ScaleFilter
from .serializers import (
    BoxartSerializer,
    BrandSerializer,
    CreateModelKitSerializer,
    ModelKitSerializer,
    ScaleSerializer,
)


class ModelKitViewSet(viewsets.ModelViewSet):
    queryset = ModelKit.objects.select_related("scale", "brand")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ModelKitSerializer
    filterset_class = ModelKitFilter

    def get_serializer_class(self):
        if self.action == "create":
            return CreateModelKitSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)


class BrandViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_class = BrandFilter
    pagination_class = None


class ScaleViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Scale.objects.all()
    serializer_class = ScaleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_class = ScaleFilter
    pagination_class = None


class BoxartViewSet(viewsets.ModelViewSet):
    queryset = Boxart.objects.none()
    serializer_class = BoxartSerializer
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES + [parsers.FileUploadParser]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data["success"] = True
        return response
