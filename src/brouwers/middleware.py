from django.http import HttpRequest
from django.utils import translation


class LocaleMiddleware:
    """
    Activate the user's preferred UI language, if set.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated and (language := request.user.ui_language):
            translation.activate(language)
        return self.get_response(request)
