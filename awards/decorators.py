from datetime import date
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.formats import date_format
from django.utils.translation import ugettext as _

from general.shortcuts import voting_enabled as _voting_enabled

def voting_enabled(view_func):
    """
    Decorator for views that checks that voting is enabled at this time. If not,
    the user is redirected to the awards homepage and a message is shown
    """

    @wraps(view_func)
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
