from django.core.cache import cache
from django.test import TestCase

from brouwers.users.tests.factory_models import UserFactory
from ..models import Preferences


class CacheTests(TestCase):
    """ Test that the cache functions correctly """
    def setUp(self):
        cache.clear()

    def test_preferences_cache(self):
        user = UserFactory()

        # log the user in
        self.client.login(username=user.username, password='password')
        self.assertEqual(Preferences.objects.filter(user=user).count(), 0)

        cache_key = 'album-preferences:%d' % user.id

        # make sure the cache is empty
        prefs = cache.get(cache_key)
        self.assertIsNone(prefs)

        # ok, get the preferences now
        prefs = Preferences.objects.get_for(user)
        self.assertTrue(isinstance(prefs, dict))

        cached_prefs = cache.get(cache_key)
        self.assertEqual(cached_prefs, prefs)

        # change preferences, make sure the cache is updated
        prefs_obj = Preferences.objects.get(user=user)
        prefs_obj.collapse_sidebar = False
        prefs_obj.save()

        cached_prefs = cache.get(cache_key)
        self.assertEqual(cached_prefs['collapse_sidebar'], prefs_obj.collapse_sidebar)
