from __future__ import unicode_literals

import unittest

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django_webtest import WebTest
from webtest.forms import Text

from brouwers.albums.tests.factories import PhotoFactory
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin
from ..models import Build
from .factories import BuildFactory


class WebTestFormSetMixin(object):

    def _add_field(self, form, name, value):
        field = Text(form, 'input', None, None, value)
        form.fields[name] = field
        form.field_order.append((name, field))
        return field


class ViewTests(WebTestFormSetMixin, LoginRequiredMixin, WebTest):

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

    def test_create(self):
        url = reverse('builds:create')
        index = self.app.get(reverse('builds:index'), status=200)

        # anonymous
        response = index.click(_('Add build'))
        self._test_login_required(url, response)

        # authenticated
        add = self.app.get(url, user=self.user, status=200)

        add.form['title'] = 'My new build'

        self.assertEqual(add.form['photos-TOTAL_FORMS'].value, '0')
        self.assertEqual(add.form['photos-INITIAL_FORMS'].value, '0')

        add.form['photos-TOTAL_FORMS'] = 2  # add two photos

        photos = PhotoFactory.create_batch(2, user=self.user)

        self._add_field(add.form, 'photos-0-id', '')
        self._add_field(add.form, 'photos-0-build', '')
        self._add_field(add.form, 'photos-0-photo', '{}'.format(photos[0].pk))
        self._add_field(add.form, 'photos-0-photo_url', '')
        self._add_field(add.form, 'photos-0-order', '')

        self._add_field(add.form, 'photos-1-id', '')
        self._add_field(add.form, 'photos-1-build', '')
        self._add_field(add.form, 'photos-1-photo', '')
        request = add.context['request']
        url = request.build_absolute_uri(photos[1].image.url)
        self._add_field(add.form, 'photos-1-photo_url', url)
        self._add_field(add.form, 'photos-1-order', '')

        response = add.form.submit()
        build = Build.objects.order_by('-pk').first()
        self.assertRedirects(response, build.get_absolute_url())

        self.assertEqual(build.photos.count(), 2)
        self.assertEqual(build.title, 'My new build')
        self.assertEqual(build.user, self.user)

    @unittest.skip('Skeleton')
    def test_update(self):

        # test add photo

        # test delete photo

        raise NotImplementedError
