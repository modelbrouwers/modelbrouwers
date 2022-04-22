from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory


class ViewTests(WebTest):
    def test_dashboard(self):
        """
        Test that the admin dashboard works as expected.
        """
        superuser = UserFactory.create(is_superuser=True, is_staff=True)
        admin = self.app.get(reverse("admin:index"), user=superuser)
        self.assertEqual(admin.status_code, 200)
