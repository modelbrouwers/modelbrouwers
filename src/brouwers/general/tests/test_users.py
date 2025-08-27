from django.test import SimpleTestCase

from ..utils import clean_username, clean_username_fallback


class UsernameTest(SimpleTestCase):
    def test_clean_username(self):
        username = "My'User"
        self.assertEqual(clean_username(username), "myʹuser")
        self.assertEqual(clean_username_fallback(username), "my user")
