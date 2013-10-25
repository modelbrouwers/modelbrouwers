from django.core.cache import cache
import models

CACHE_KEY = 'current_bans'

def set_banning_cache(qs=None):
    if qs is None:
        qs = models.Ban.get_bans_queryset()
    bans = qs.order_by('-expiry_date')
    cache.set(CACHE_KEY, list(bans), 60*60*24) # cache 24 hours
