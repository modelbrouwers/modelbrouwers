from datetime import date
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import available_attrs
from django.utils.formats import date_format
from django.utils.translation import ugettext as _

from general.shortcuts import voting_enabled as _voting_enabled

def real_voting_enabled(view_func):
    """
    Decorator for views that checks that voting is enabled at this time. If not,
    the user is redirected to the awards homepage and a message is shown
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if _voting_enabled():
                return view_func(request, *args, **kwargs)
            else:
                this_year = date.today().year
                vote_start_date = date(this_year+1, 1, 1)
                vote_end_date = date(this_year+1, settings.VOTE_END_MONTH, settings.VOTE_END_DAY)
                message = _("Voting is enabled from %(start_date)s until %(end_date)s.") % {
                    'start_date': date_format(vote_start_date),
                    'end_date': date_format(vote_end_date),
                }
                messages.error(request, message)
            return redirect(reverse('awards_index'))
        return _wrapped_view
    return decorator


def voting_enabled(view_func):
    actual_decorator = real_voting_enabled
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


# def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
#     """
#     Decorator for views that checks that the user passes the given test,
#     redirecting to the log-in page if necessary. The test should be a callable
#     that takes the user object and returns True if the user passes.
#     """

#     def decorator(view_func):
#         @wraps(view_func, assigned=available_attrs(view_func))
#         def _wrapped_view(request, *args, **kwargs):
#             if test_func(request.user):
#                 return view_func(request, *args, **kwargs)
#             path = request.build_absolute_uri()
#             # If the login url is the same scheme and net location then just
#             # use the path as the "next" url.
#             login_scheme, login_netloc = urlparse.urlparse(login_url or
#                                                         settings.LOGIN_URL)[:2]
#             current_scheme, current_netloc = urlparse.urlparse(path)[:2]
#             if ((not login_scheme or login_scheme == current_scheme) and
#                 (not login_netloc or login_netloc == current_netloc)):
#                 path = request.get_full_path()
#             from django.contrib.auth.views import redirect_to_login
#             return redirect_to_login(path, login_url, redirect_field_name)
#         return _wrapped_view
#     return decorator
