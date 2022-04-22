from django.urls import path, re_path
from django.views.generic import RedirectView

# from .ajax_views import RotateView
from .views import (
    AlbumCreateView,
    AlbumDeleteView,
    AlbumDetailView,
    AlbumDownloadView,
    AlbumListView,
    AlbumRestoreView,
    AlbumUpdateView,
    IndexView,
    MyAlbumsView,
    PhotoDeleteView,
    PhotoDetailView,
    PhotoRestoreView,
    PhotoUpdateView,
    PreferencesUpdateView,
    UploadView,
)

app_name = "albums"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("new/", AlbumCreateView.as_view(), name="create"),
    path("list/", RedirectView.as_view(pattern_name="albums:all", permanent=True)),
    path("all/", AlbumListView.as_view(), name="all"),
    path("mine/", MyAlbumsView.as_view(), name="mine"),
    path(
        "my_gallery/", RedirectView.as_view(pattern_name="albums:mine", permanent=True)
    ),
    re_path(
        r"^album/\{?(?P<pk>\d+)\}?/$", AlbumDetailView.as_view(), name="detail"
    ),  # curly braces for Javascript url
    path("album/<int:pk>/edit/", AlbumUpdateView.as_view(), name="update"),
    path("album/<int:pk>/delete/", AlbumDeleteView.as_view(), name="delete"),
    path("album/<int:pk>/restore/", AlbumRestoreView.as_view(), name="restore"),
    path("album/<int:pk>/page/<int:page>/", AlbumDetailView.as_view(), name="detail"),
    path("album/<int:pk>/download/", AlbumDownloadView.as_view(), name="download"),
    path("photo/<int:pk>/", PhotoDetailView.as_view(), name="photo-detail"),
    path("photo/<int:pk>/edit/", PhotoUpdateView.as_view(), name="photo_update"),
    path("photo/<int:pk>/delete/", PhotoDeleteView.as_view(), name="photo_delete"),
    path("photo/<int:pk>/restore/", PhotoRestoreView.as_view(), name="photo_restore"),
    path("upload/", UploadView.as_view(), name="upload"),
    path("settings/", PreferencesUpdateView.as_view(), name="settings"),
    path(
        "preferences/",
        RedirectView.as_view(pattern_name="albums:settings", permanent=True),
    ),
]
