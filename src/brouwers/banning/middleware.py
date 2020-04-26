import logging

from django.contrib.auth import logout
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from brouwers.general.utils import get_client_ip

from .models import Ban
from .utils import CACHE_KEY, set_banning_cache

logger = logging.getLogger(__name__)


class BanningMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def _get_bans(self, request):
        user = request.user
        ip = get_client_ip(request)

        ban_list = cache.get(CACHE_KEY)

        if ban_list is None:
            bans = Ban.get_bans_queryset()
            # set cache
            set_banning_cache(bans)

            filters = Q(ip=ip)
            if user.is_authenticated:
                filters = filters | Q(user_id=user.id)

            bans = bans.filter(filters)
            if bans.exists():
                ban_list = bans.order_by('-expiry_date')
        else:
            now = timezone.now()

            def _ban_relevant(ban) -> bool:
                if ban.expiry_date and ban.expiry_date < now:
                    return False
                if user.is_authenticated and ban.user_id == user.id:
                    return True
                return ban.ip == ip

            ban_list = [ban for ban in ban_list if _ban_relevant(ban)]

        return ban_list

    def __call__(self, request):
        # allow logins
        if request.path == reverse('users:login'):
            return self.get_response(request)

        user = request.user
        # NEVER ban superusers
        if (user.is_authenticated and user.is_superuser):
            return self.get_response(request)

        ban_list = self._get_bans(request)
        if ban_list:
            logout(request)
            return render(request, 'banning/banned.html', {'bans': ban_list}, status=403)

        return self.get_response(request)
