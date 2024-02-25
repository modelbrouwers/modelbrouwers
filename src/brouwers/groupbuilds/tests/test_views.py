from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from .factories import GroupBuildFactory


class ViewTests(WebTest):
    def test_detail_page(self):
        gb = GroupBuildFactory.create()
        gb.admins.add(gb.applicant)
        url = gb.get_absolute_url()

        # anonymous user
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(gb.theme, response)

        # login as owner user
        response = self.app.get(url, user=gb.applicant)
        self.assertEqual(response.status_code, 200)

        # and as superuser
        superuser = UserFactory.create(is_staff=True, is_superuser=True)
        response = self.app.get(url, user=superuser)
        self.assertEqual(response.status_code, 200)
