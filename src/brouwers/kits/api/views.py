from rest_framework import viewsets

from ..models import ModelKit
from .serializers import ModelKitSerializer
from .filters import ModelKitFilter


class ModelKitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelKit.objects.all()
    serializer_class = ModelKitSerializer
    filter_class = ModelKitFilter
