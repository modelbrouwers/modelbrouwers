from datetime import date

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _, ungettext as _n
from django.views.decorators.cache import cache_page
from django.views.generic import View

from brouwers.general.decorators import (
    login_required_403, user_passes_test_403
)
from brouwers.general.models import UserProfile
from brouwers.general.utils import (
    clean_username, clean_username_fallback, get_username_for_user
)

from .forms import ForumForm, PosterIDsForm
from .models import (
    BuildReportsForum, ForumLinkBase, ForumPostCountRestriction, ForumUser,
    Report
)


class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        cache = cache_page(self.get_cache_timeout())
        return cache(super(CacheMixin, self).dispatch)(*args, **kwargs)


class SyncDataView(View):
    cache_timeout = 60 * 60 * 24

    def get(self, request, *args, **kwargs):
        today = date.today()
        links_to_be_synced = (
            ForumLinkBase.objects
            .filter(enabled=True, to_date__gte=today, from_date__lte=today)
            .prefetch_related('forumlinksynced_set')
        )
        data = {
            link.link_id: [l.link_id for l in link.forumlinksynced_set.all()]
            for link in links_to_be_synced
        }
        return JsonResponse(data)


class ChatView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            nickname = get_username_for_user(request.user)
        else:
            nickname = settings.IRC_DEFAULT_NICK

        html = render_to_string('chat.html', {
            'MIBBIT_SETTINGS': settings.MIBBIT_SETTINGS,
            'IRC_SERVER': settings.IRC_SERVER,
            'IRC_CHANNEL': settings.IRC_CHANNEL,
            'nickname': nickname,
        })
        return JsonResponse({
            'html': html,
            'title': "Brouwers chat [%s, %s]" % (settings.IRC_SERVER, settings.IRC_CHANNEL)
        })


class ModDataView(PermissionRequiredMixin, View):
    permission_required = 'forum_tools.can_see_reports'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        count = Report.objects.filter(report_closed=False).count()
        data = {
            'open_reports': count,
            'text_reports': _n(
                "1 open report",
                "%(num)d open reports",
                count
            ) % {'num': count}
        }
        return JsonResponse(data)


@user_passes_test_403(lambda u: u.groups.filter(name__iexact='content sharing').exists())
def get_sharing_perms(request):
    data = {}
    form = PosterIDsForm(request.GET)
    if form.is_valid():
        forumusers = ForumUser.objects.filter(user_id__in=form.poster_ids)

        if forumusers:
            # render text in template
            allowed = render_to_string('forum_tools/sharing_allowed.html')
            not_allowed = render_to_string('forum_tools/sharing_not_allowed.html')

            # manual 'joining' on username
            usernames = [forum_user.username for forum_user in forumusers]
            profiles = {
                profile.nickname: profile
                for profile in UserProfile.objects.filter(forum_nickname__in=usernames)
            }

            for forumuser in forumusers:
                profile = profiles.get(forumuser.username)
                data[forumuser.user_id] = allowed if (profile and profile.allow_sharing) else not_allowed

    return JsonResponse(data)


@login_required_403
def get_posting_level(request):
    data = {}
    form = ForumForm(request.GET)
    if form.is_valid():
        forum = form.cleaned_data['forum']
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
        data['restrictions'] = [restr.posting_level for restr in restrictions if restr.min_posts > num_posts]
    return JsonResponse(data)


class BuildReportForumsView(CacheMixin, View):
    cache_timeout = 60 * 60 * 24 * 7 * 2

    def get(self, request, *args, **kwargs):
        # TODO: return data if the build report was added already
        forum_ids = BuildReportsForum.objects.values_list('forum_id', flat=True)
        data = {
            'forum_ids': list(forum_ids),
            'text_build_report': _('Add build report'),
            'text_nominate': _('Nominate for award'),
        }
        return JsonResponse(data)
