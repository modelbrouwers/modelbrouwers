from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django_webtest import WebTest
from webtest.forms import Text

from brouwers.albums.tests.factories import PhotoFactory
from brouwers.forum_tools.tests.factories import TopicFactory
from brouwers.kits.tests.factories import ModelKitFactory
from brouwers.users.tests.factories import UserFactory
from brouwers.utils.tests.mixins import LoginRequiredMixin
from ..models import Build
from .factories import BuildFactory, BuildPhotoFactory


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

        # add some kits
        kits = ModelKitFactory.create_batch(2)
        for kit in kits:
            self._add_field(add.form, 'kits', kit.pk)

        response = add.form.submit()
        build = Build.objects.order_by('-pk').first()
        self.assertRedirects(response, build.get_absolute_url())

        self.assertEqual(build.photos.count(), 2)
        self.assertEqual(build.title, 'My new build')
        self.assertEqual(build.user, self.user)
        self.assertEqual(build.kits.count(), 2)

    def test_update(self):
        """
        Tests that updating builds works as expected.

        It should be possible to add/remove kits of a build
        """
        kits = ModelKitFactory.create_batch(2)
        build = BuildFactory.create(user=self.user, kits=kits)
        build_photo = BuildPhotoFactory.create(photo_url='http://i.imgur.com/asdljfo.jpg', build=build)

        url = reverse('builds:update', kwargs={'slug': build.slug})

        # test that non-auth can't update
        response = self.app.get(url)
        self.assertRedirects(response, '{}?next={}'.format(settings.LOGIN_URL, url))

        # test that different user can't update
        other_user = UserFactory.create()
        self.app.get(url, user=other_user, status=404)

        # owner
        page = self.app.get(url, user=self.user, status=200)

        kit_fields = page.form.fields.get('kits')
        self.assertEqual(len(kit_fields), build.kits.count())

        # delete a kit
        pk = int(kit_fields[0].value)
        kit_fields[0].checked = False

        # test add photo
        self.assertEqual(page.form['photos-TOTAL_FORMS'].value, '1')
        self.assertEqual(page.form['photos-INITIAL_FORMS'].value, '1')

        photo = PhotoFactory.create(user=self.user)
        page.form['photos-TOTAL_FORMS'] = 2
        self._add_field(page.form, 'photos-1-id', '')
        self._add_field(page.form, 'photos-1-build', '')
        self._add_field(page.form, 'photos-1-photo', '{}'.format(photo.pk))
        self._add_field(page.form, 'photos-1-photo_url', '')
        self._add_field(page.form, 'photos-1-order', '')

        # test delete photo
        page.form['photos-0-DELETE'].checked = True

        redirect = page.form.submit()
        self.assertRedirects(redirect, build.get_absolute_url())

        build.refresh_from_db()

        kits = build.kits.all()
        self.assertEqual(kits.count(), 1)
        self.assertFalse(kits.filter(pk=pk).exists())

        # check photos
        self.assertEqual(build.photos.count(), 1)
        self.assertNotEqual(build.photos.get(), build_photo)

    def test_create_from_external(self):
        """
        Asserts that the button with prefilled fields works correctly.
        """
        topic = TopicFactory.create()
        url = '{}?forum_id={}&topic_id={}&title=Dummy%20title'.format(
            reverse('builds:create'),
            topic.forum.pk,
            topic.pk
        )

        page = self.app.get(url, user=self.user, status=200)

        self.assertEqual(page.form['title'].value, 'Dummy title')
        self.assertEqual(page.form['topic'].value, 'http://example.com/phpBB3/viewtopic.php?t={}'.format(topic.pk))
