from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext as _, ngettext as _n
from django.views.decorators.cache import cache_page
from django.views.generic import View

from brouwers.general.decorators import login_required_403
from brouwers.general.utils import clean_username, clean_username_fallback

from .forms import ForumForm
from .models import BuildReportsForum, ForumPostCountRestriction, ForumUser, Report


class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        cache = cache_page(self.get_cache_timeout())
        return cache(super().dispatch)(*args, **kwargs)


class ModDataView(PermissionRequiredMixin, View):
    permission_required = "forum_tools.can_see_reports"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        count = Report.objects.filter(report_closed=False).count()
        data = {
            "open_reports": count,
            "text_reports": _n("1 open report", "%(num)d open reports", count)
            % {"num": count},
        }
        return JsonResponse(data)


@login_required_403
def get_posting_level(request):
    data = {}
    form = ForumForm(request.GET)
    if form.is_valid():
        forum = form.cleaned_data["forum"]
        username = request.user.username
        # iexact doesn't work because MySQL tables are utf8_bin collated...
        try:
            username_cleaned = clean_username(username)
            forum_user = ForumUser.objects.get(username_clean=username_cleaned)
        except ForumUser.DoesNotExist:
            try:
                username_cleaned = clean_username_fallback(username)
                forum_user = ForumUser.objects.get(username_clean=username_cleaned)
            except ForumUser.DoesNotExist:
                # final fallback - try to read the cookie
                uid = request.COOKIES.get(settings.PHPBB_UID_COOKIE)
                forum_user = ForumUser.objects.get(pk=uid)

        # TODO: find a way to cache this... or find it out client side
        num_posts = forum_user.user_posts

        restrictions = ForumPostCountRestriction.objects.filter(forum_id=forum.forum_id)
        data["restrictions"] = [
            restr.posting_level for restr in restrictions if restr.min_posts > num_posts
        ]
    return JsonResponse(data)


class BuildReportForumsView(CacheMixin, View):
    cache_timeout = 60 * 60 * 24 * 7 * 2

    def get(self, request, *args, **kwargs):
        # TODO: return data if the build report was added already
        forum_ids = BuildReportsForum.objects.values_list("forum_id", flat=True)
        data = {
            "forum_ids": list(forum_ids),
            "text_build_report": _("Add build report"),
            "text_nominate": _("Nominate for award"),
        }
        return JsonResponse(data)
