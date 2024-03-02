from typing import Any, Protocol

from django.http import HttpRequest
from django.http.response import HttpResponseBase


class ViewFunc(Protocol):
    args: tuple
    kwargs: dict
    view_class: type

    def __call__(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponseBase: ...  # pragma: nocover


def view_instance(view: ViewFunc, *args, **kwargs):
    """
    Return a CBV instance from the callback with the specified *args and **kwargs.
    """
    instance = view.view_class()
    instance.args = args
    instance.kwargs = kwargs
    return instance
