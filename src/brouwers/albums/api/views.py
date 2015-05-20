from rest_framework import parsers, permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ..models import Photo
from .filters import PhotoFilter
from .serializers import PhotoSerializer, UploadPhotoSerializer
from .renderers import FineUploaderRenderer
from .pagination import PhotoPagination


class PhotoViewSet(viewsets.ModelViewSet):
    """
    View to handle HTML5 file uploads.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (parsers.FileUploadParser,)
    queryset = Photo.objects.exclude(trash=True).exclude(album__public=False)
    serializer_class = PhotoSerializer
    filter_class = PhotoFilter
    pagination_class = PhotoPagination

    def get_renderers(self):
        if self.request.method == 'POST':
            return [FineUploaderRenderer()]
        return super(PhotoViewSet, self).get_renderers()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UploadPhotoSerializer
        return super(PhotoViewSet, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        Overwritten to comply with FineUploader's demands for the response.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            response_data = serializer.data
            response_data.update({'success': True})
            return Response(response_data, status=status.HTTP_200_OK, headers=headers)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    def next_or_previous(self, request, next=True, *args, **kwargs):
        attr = 'next' if next else 'previous'
        current = self.get_object()
        qs = getattr(Photo.objects, attr)
        photo = qs(current, user=self.request.user)
        serializer = self.get_serializer(photo)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def next(self, request, *args, **kwargs):
        return self.next_or_previous(request, next=True, *args, **kwargs)

    @detail_route(methods=['get'])
    def previous(self, request, *args, **kwargs):
        return self.next_or_previous(request, next=False, *args, **kwargs)
