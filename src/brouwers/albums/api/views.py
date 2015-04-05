from rest_framework import parsers, permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Photo
from .serializers import PhotoSerializer
from .renderers import FineUploaderRenderer


class PhotoViewSet(viewsets.ModelViewSet):
    """
    View to handle HTML5 file uploads.
    """
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.FileUploadParser,)
    queryset = Photo.objects.none()
    serializer_class = PhotoSerializer

    def get_renderers(self):
        if self.request.method == 'POST':
            return [FineUploaderRenderer()]
        return super(PhotoViewSet, self).get_renderers()

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
