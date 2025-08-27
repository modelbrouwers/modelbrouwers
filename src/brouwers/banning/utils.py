import logging

from django.core.cache import cache

from . import models

logger = logging.getLogger(__name__)

CACHE_KEY = "current_bans"


def set_banning_cache(qs=None):
    if qs is None:
        qs = models.Ban.get_bans_queryset()

    bans = list(qs)
    logger.debug("Setting bans cache: %d objects", len(bans))
    cache.set(CACHE_KEY, bans, 60 * 60 * 24)  # cache 24 hours
