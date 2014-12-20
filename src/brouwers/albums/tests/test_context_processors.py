from django.test import TestCase
from django.http import HttpRequest
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user

from brouwers.albums.context_processors import user_is_album_admin
from brouwers.albums.models import Preferences
from brouwers.albums.serializers import PreferencesSerializer


class ContextProcessorTests(TestCase):

    def test_user_is_album_admin(self):
        """ Tests the albums.context_processors.user_is_admin context processor """
        request = HttpRequest()
        request.session = self.client.session
        request.user = SimpleLazyObject(lambda: get_user(request))

        data = user_is_album_admin(request)
        expected_data = {
            'user_is_album_admin': False,
            'album_preferences': PreferencesSerializer(Preferences()).data,
        }
        self.assertEquals(data, expected_data)
