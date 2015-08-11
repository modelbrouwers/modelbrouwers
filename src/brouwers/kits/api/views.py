from rest_framework import viewsets

from ..models import ModelKit
from .serializers import ModelKitSerializer
from .filters import ModelKitFilter


class ModelKitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModelKit.objects.select_related('scale', 'brand')
    serializer_class = ModelKitSerializer
    filter_class = ModelKitFilter
