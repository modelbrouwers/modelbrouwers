from rest_framework.pagination import PageNumberPagination


class PageNumberPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        response = super(PageNumberPagination, self).get_paginated_response(data)
        response.data['paginate_by'] = self.get_page_size(self.request)
        return response
