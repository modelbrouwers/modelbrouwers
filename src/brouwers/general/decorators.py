from functools import wraps

from django.core.exceptions import PermissionDenied
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


def permission_required_ajax(perm, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if neccesary.
    Normally and empty HttpResponseForbidden is returned.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        # First check if the user has the permission (even anon users)
        if user.has_perm(perm):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, return HttpResponseForbidden through user_passes_test_403
        return False
    return user_passes_test_403(check_perms)
