from brouwers.api.pagination import PageNumberPagination
from ..views import AlbumDetailView


class PhotoPagination(PageNumberPagination):
    page_size = AlbumDetailView.paginate_by
    page_size_query_param = 'page_size'
    max_page_size = 50
