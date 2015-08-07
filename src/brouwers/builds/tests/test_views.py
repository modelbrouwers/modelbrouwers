from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

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
        builds = index.context['builds']
        expected_builds = self.builds
        expected_builds.reverse()
        self.assertQuerysetEqual(builds, [
            repr(x) for x in expected_builds
        ])

    def test_user_list(self):
        user_builds = BuildFactory.create_batch(2, user=self.user)
        index_url = reverse('builds:index')
        url = reverse('builds:user_build_list', kwargs={'user_id': self.user.id})

        # anonymous
        index = self.app.get(index_url, status=200)
        self.assertNotContains(index, _('My builds'))

        # authenticated
        index = self.app.get(index_url, status=200, user=self.user)
        self.assertContains(index, _('My builds'))
        self.assertContains(index, url)
        my_builds = index.click(_('My builds'))
        self.assertEqual(my_builds.status_code, 200)
        self.assertQuerysetEqual(
            my_builds.context['builds'],
            reversed([repr(x) for x in user_builds])
        )
        self.assertEqual(my_builds.context['request'].path, url)

    def test_detail(self):
        build = BuildFactory.create()
        detail = self.app.get(build.get_absolute_url(), status=200)
        self.assertEqual(detail.context['build'], build)
