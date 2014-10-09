from django_webtest import WebTest

from users.tests.factory_models import UserFactory
from .factories import GroupBuildFactory


class ViewTests(WebTest):

    def test_detail_page(self):
        gb = GroupBuildFactory.create()
        gb.admins.add(gb.applicant)
        url = gb.get_absolute_url()

        # anonymous user
        response = self.app.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIn(gb.theme, response)
        self.assertFalse(response.context['can_edit'])

        # login as owner user
        response = self.app.get(url, user=gb.applicant)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['can_edit'])

        # and as superuser
        superuser = UserFactory.create(is_staff=True, is_superuser=True)
        response = self.app.get(url, user=superuser)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['can_edit'])
