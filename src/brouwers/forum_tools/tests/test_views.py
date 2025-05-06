from django.test import TestCase
from django.urls import reverse

from brouwers.users.tests.factories import UserFactory


class ForumToolsViewTests(TestCase):

    def test_get_sync_data(self):
        url = reverse("forum_tools:get_sync_data")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_mod_data_anon(self):
        url = reverse("forum_tools:get_mod_data")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_get_mod_data_mod(self):
        url = reverse("forum_tools:get_mod_data")
        user = UserFactory.create(is_superuser=True)
        self.client.force_login(user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_sharing_perms(self):
        url = reverse("forum_tools:get_sharing_perms")
        user = UserFactory.create(is_superuser=True)
        user.groups.create(name="content sharing")
        self.client.force_login(user)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_build_report_forums(self):
        url = reverse("forum_tools:get_build_report_forums")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
