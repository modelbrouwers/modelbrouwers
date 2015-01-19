import logging

from django.core.cache import cache
from django.utils import timezone

from . import models

logger = logging.getLogger(__name__)

CACHE_KEY = 'current_bans'


def set_banning_cache(qs=None):
    if qs is None:
        qs = models.Ban.get_bans_queryset()

    bans = list(qs)
    invalid_tz_bans = filter(lambda ban: ban.expiry_date is not None and ban.expiry_date.tzinfo is None, bans)
    if len(invalid_tz_bans):
        logger.warn('Detected %d invalid tz bans.' % len(invalid_tz_bans))
    for ban in invalid_tz_bans:
        ban.expiry_date = ban.expiry_date.replace(tzinfo=timezone.utc)

    logger.debug('Setting bans cache: %d objects' % len(bans))
    cache.set(CACHE_KEY, bans, 60*60*24) # cache 24 hours
