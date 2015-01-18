from django.core.cache import cache
from django.utils import timezone

import models

CACHE_KEY = 'current_bans'

def set_banning_cache(qs=None):
    if qs is None:
        qs = models.Ban.get_bans_queryset()
    bans = list(qs.order_by('-expiry_date'))
    # FIXME: sometimes the timezone doesn't get set...
    for ban in [ban for ban in bans if
                ban.expiry_date is not None
                and ban.expiry_date.tzinfo is None]:
        bans.expiry_date.replace(tzinfo=timezone.utc)
    cache.set(CACHE_KEY, bans, 60*60*24) # cache 24 hours
