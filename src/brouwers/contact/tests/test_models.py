from django.test import SimpleTestCase

from ..models import ContactMessage


class ModelTests(SimpleTestCase):
    def test_str_method(self):
        contact_message = ContactMessage(name="Dolan", message="A" * 100)

        self.assertIn("Dolan", str(contact_message))
