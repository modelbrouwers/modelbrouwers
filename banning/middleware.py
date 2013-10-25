from django.contrib.auth import logout
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render

from general.utils import get_client_ip

from models import Ban
from utils import CACHE_KEY, set_banning_cache
from datetime import datetime

class BanningMiddleware(object):
    def process_request(self, request):
        # allow logins
        if request.path == reverse('general.views.custom_login'):
            return None
        u = request.user
        ip = get_client_ip(request)
        
        ban_list = cache.get(CACHE_KEY)
                
        if ban_list is None:
            bans = Ban.get_bans_queryset()
            qs = bans
            
            if u.is_authenticated():
                bans = bans.filter(Q(user_id=u.id) | Q(ip=ip))
            else:
                bans = bans.filter(ip=ip)

            if bans.exists():
                ban_list = bans.order_by('-expiry_date')

            # set cache
            set_banning_cache(qs)
        else:
            # checking if there are active bans for our current user
            # anonymous users: check ip
            if u.is_authenticated():
                ban_list = [ban for ban in ban_list if ban.user_id==u.id or ban.ip==ip]
            else:
                ban_list = [ban for ban in ban_list if ban.ip==ip]

            ban_list = [ban for ban in ban_list 
                        if ban.expiry_date is None
                        or ban.expiry_date >= datetime.now()]
        
        # NEVER ban superusers
        if ban_list and not (u.is_authenticated() and u.is_superuser):
            logout(request)
            return render(request, 'banning/banned.html', {'bans': ban_list}, status=403)
        return None