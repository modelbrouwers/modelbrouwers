from .edit import (
    AlbumCreateView, AlbumDeleteView, AlbumRestoreView, AlbumUpdateView,
    PhotoDeleteView, PhotoUpdateView, PhotoRestoreView,
    PreferencesUpdateView, UploadView
)
from .public import (
    IndexView, AlbumListView, AlbumDetailView, PhotoDetailView, AlbumDownloadView
)
from .private import MyAlbumsView
