from rest_framework import parsers, permissions
from rest_framework import viewsets

from ..models import Photo


class PhotoViewSet(viewsets.ModelViewSet):
    """
    View to handle HTML5 file uploads.
    """
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FileUploadParser,)
    queryset = Photo.objects.all()
