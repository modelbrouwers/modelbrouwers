from rest_framework.response import Response
from rest_framework.views import APIView

from ..forms import BuildSearchForm


class SearchView(APIView):
    """
    API endpoint for autocomplete search.

    Returns exact matches for usernames first, and then builds that
    soft match the query term.
    """

    def get(self, request, *args, **kwargs):
        form = BuildSearchForm(data=request.GET)
        if not form.is_valid():
            return Response(form.errors)
        return Response(form.get_search_results())
