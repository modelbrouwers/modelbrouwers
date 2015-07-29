from django.core.urlresolvers import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory
from .factories import BuildFactory


class ViewTests(WebTest):

    def setUp(self):
        self.user = UserFactory.create()
        self.builds = BuildFactory.create_batch(5)

    def test_index(self):
        url = reverse('builds:index')
        index = self.app.get(url, status=200)
