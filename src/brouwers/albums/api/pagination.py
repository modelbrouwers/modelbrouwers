from brouwers.api.pagination import PageNumberPagination

from ..models import Preferences
from ..views import AlbumDetailView


class PhotoPagination(PageNumberPagination):
    page_size = AlbumDetailView.paginate_by
    page_size_query_param = "page_size"
    max_page_size = 50


class MyPhotoPagination(PageNumberPagination):
    """
    Custom paginator where max_page_size is configurable via user settings.
    """

    def get_page_size(self, request):
        prefs = Preferences.objects.get_for(request.user)
        return prefs["paginate_by_sidebar"]
