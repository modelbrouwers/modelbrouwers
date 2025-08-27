# ruff: noqa: F403
import os

os.environ.setdefault("SESSION_COOKIE_DOMAIN", "staging.modelbrouwers.nl")
os.environ.setdefault("ALLOWED_HOSTS", "staging.modelbrouwers.nl")
os.environ.setdefault("CACHE_PREFIX", "staging")

from .production import *
