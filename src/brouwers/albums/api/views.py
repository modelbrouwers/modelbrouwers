from django.db.models import Q

from rest_framework import parsers, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.settings import api_settings

from ..models import Album, Photo, Preferences
from .filters import PhotoFilter
from .pagination import MyPhotoPagination, PhotoPagination
from .renderers import FineUploaderRenderer
from .serializers import (
    AlbumSerializer,
    ForumPhotoSerializer,
    PhotoSerializer,
    PreferencesSerializer,
    UploadPhotoSerializer,
)


class PhotoViewSet(viewsets.ModelViewSet):
    """
    View to handle HTML5 file uploads and photo manipulations such as
    rotating the photo.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES + [parsers.FileUploadParser]
    queryset = Photo.objects.exclude(trash=True).select_related("user")
    serializer_class = PhotoSerializer
    filterset_class = PhotoFilter
    pagination_class = PhotoPagination

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(
                Q(album__public=True) | Q(album__user=self.request.user)
            )
        return self.queryset.exclude(album__public=False)

    def get_renderers(self):
        if self.action == "create":
            return [FineUploaderRenderer()]
        return super().get_renderers()

    def get_serializer_class(self):
        if self.action == "create":
            return UploadPhotoSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        Overwritten to comply with FineUploader's demands for the response.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=self.request.user)
            headers = self.get_success_headers(serializer.data)
            response_data = serializer.data
            response_data.update({"success": True})
            return Response(response_data, status=status.HTTP_200_OK, headers=headers)
        return Response(
            {"success": False}, status=status.HTTP_400_BAD_REQUEST
        )  # pragma: no cover

    @action(detail=True, methods=["patch"])
    def rotate(self, request, *args, **kwargs):
        photo = self.get_object()
        direction = request.data.get("direction")
        if direction not in ["cw", "ccw"]:
            raise ValidationError("The direction must be set to 'cw' or 'ccw'")
        degrees = -90 if direction == "cw" else 90
        photo.rotate(degrees=degrees)
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)


class PreferencesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Must always return the settings for the (logged in) user making the
    api request.
    """

    queryset = Preferences.objects.none()
    serializer_class = PreferencesSerializer
    pagination_class = None
    lookup_value_regex = "self"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Preferences.objects.filter(user=self.request.user)
        return super().get_queryset()

    def get_object(self):
        return Preferences.objects.get_for(self.request.user)

    def retrieve(self, request, *args, **kwargs):
        # from cache, or populates cache, thus already serialized
        return Response(self.get_object())


class MyAlbumsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.none()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AlbumSerializer
    pagination_class = None

    def get_queryset(self):
        return Album.objects.for_user(self.request.user)


class MyPhotosViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Photo.objects.none()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ForumPhotoSerializer
    filterset_class = PhotoFilter
    pagination_class = MyPhotoPagination

    def get_queryset(self):
        return Photo.objects.for_user(self.request.user).order_by("-uploaded")

    @action(detail=True, methods=["post"])
    def set_cover(self, request, *args, **kwargs):
        photo = self.get_object()
        photo.album.cover = photo
        photo.album.save()
        serializer = self.get_serializer(photo)
        return Response(serializer.data)
