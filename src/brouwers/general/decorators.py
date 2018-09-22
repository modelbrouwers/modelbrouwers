from functools import wraps

from django.http import HttpResponseForbidden
from django.utils.decorators import available_attrs


def user_passes_test_403(test_func):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return decorator


def login_required_403(function=None):
    actual_decorator = user_passes_test_403(
        lambda u: u.is_authenticated
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
