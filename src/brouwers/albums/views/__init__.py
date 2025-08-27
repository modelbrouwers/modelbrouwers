from .edit import (
    AlbumCreateView,
    AlbumDeleteView,
    AlbumRestoreView,
    AlbumUpdateView,
    PhotoDeleteView,
    PhotoRestoreView,
    PhotoUpdateView,
    PreferencesUpdateView,
    UploadView,
)
from .private import MyAlbumsView
from .public import (
    AlbumDetailView,
    AlbumDownloadView,
    AlbumListView,
    IndexView,
    PhotoDetailView,
    SearchView,
)

__all__ = [
    "AlbumCreateView",
    "AlbumDeleteView",
    "AlbumRestoreView",
    "AlbumUpdateView",
    "PhotoDeleteView",
    "PhotoRestoreView",
    "PhotoUpdateView",
    "PreferencesUpdateView",
    "UploadView",
    "MyAlbumsView",
    "AlbumDetailView",
    "AlbumDownloadView",
    "AlbumListView",
    "IndexView",
    "PhotoDetailView",
    "SearchView",
]
