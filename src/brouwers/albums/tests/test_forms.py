from django.test import TestCase

from brouwers.albums.models import Category
from brouwers.users.tests.factory_models import UserFactory


class FormTests(TestCase):

    def test_album_form(self):
        from ..forms import AlbumForm

        user = UserFactory.create()

        form = AlbumForm(data={}, user=user)
        self.assertEquals(form.user, user)

        form = AlbumForm(data={}, initial={'user': user})
        self.assertEquals(form.user, user)

        form = AlbumForm(data={}, initial={})
        self.assertIsNone(form.user)

        form = AlbumForm()
        self.assertIsNone(form.user)

        # test that the category queryset is correct
        qs = Category.objects.filter(public=True)
        form = AlbumForm(admin_mode=False)
        self.assertEquals(list(form.fields['category'].queryset), list(qs))

        form = AlbumForm(user=user)
        self.assertEquals(list(form.fields['category'].queryset), list(qs))

        # clean the build report url
        url1 = 'http://www.modelbrouwers.nl/phpBB3/viewtopic.php?f=1&t=1'
        url2 = 'http://modelbrouwers.nl/phpBB3/viewtopic.php?a=1&b=1'
        url3 = ''

        f1 = AlbumForm(data={'build_report': url1})
        f1.is_valid()
        self.assertEquals(f1.cleaned_data['build_report'], url1)

        f2 = AlbumForm(data={'build_report': url2})
        f2.is_valid()
        self.assertTrue(len(f2.errors['build_report']) > 0)

        f3 = AlbumForm(data={'build_report': url3})
        f3.is_valid()
        self.assertEquals(f3.cleaned_data['build_report'], '')
