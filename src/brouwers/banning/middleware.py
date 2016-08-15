import logging

from django.contrib.auth import logout
from django.core.cache import cache
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from brouwers.general.utils import get_client_ip
from .models import Ban
from .utils import CACHE_KEY, set_banning_cache

logger = logging.getLogger(__name__)


class BanningMiddleware(object):
    def process_request(self, request):
        # allow logins
        if request.path == reverse('users:login'):
            return None

        u, ip = request.user, get_client_ip(request)
        ban_list = cache.get(CACHE_KEY)

        if ban_list is None:
            bans = Ban.get_bans_queryset()
            qs = bans

            if u.is_authenticated:
                bans = bans.filter(Q(user_id=u.id) | Q(ip=ip))
            else:
                bans = bans.filter(ip=ip)

            if bans.exists():
                ban_list = bans.order_by('-expiry_date')

            # set cache
            set_banning_cache(qs)
        else:
            invalid_tz = filter(lambda b: b.expiry_date and b.expiry_date.tzinfo is None, ban_list)
            if len(invalid_tz):
                logger.warn('%d bans with timezone naive expiry dates' % len(invalid_tz))
                for ban in invalid_tz:
                    ban.expiry_date = ban.expiry_date.replace(tzinfo=timezone.utc)

            # checking if there are active bans for our current user
            # anonymous users: check ip
            if u.is_authenticated:
                filter_ = lambda ban: ban.user_id == u.id or ban.ip == ip
            else:
                filter_ = lambda ban: ban.ip == ip

            now = timezone.now()
            filter_date = lambda ban: ban.expiry_date is None or ban.expiry_date >= now
            ban_list = filter(filter_date, filter(filter_, ban_list))

        # NEVER ban superusers
        if ban_list and not (u.is_authenticated and u.is_superuser):
            logout(request)
            return render(request, 'banning/banned.html', {'bans': ban_list}, status=403)
        return None
