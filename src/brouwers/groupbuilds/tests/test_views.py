from django_webtest import WebTest

from ..constants import GroupbuildStatuses
from .factories import GroupBuildFactory


class ViewTests(WebTest):
    def test_detail_page(self):
        gb = GroupBuildFactory.create(status=GroupbuildStatuses.accepted)
        url = gb.get_absolute_url()

        # anonymous user
        response = self.app.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(gb.theme, response)
