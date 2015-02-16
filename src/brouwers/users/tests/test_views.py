from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django_webtest import WebTest

from brouwers.users.tests.factory_models import UserFactory


class ProfileTests(WebTest):

    def setUp(self):
        super(ProfileTests, self).setUp()
        self.user = UserFactory.create()

    def test_edit_profile_login(self):
        """ Test that login is required to edit the profile """
        url = reverse('profile')
        redirect = self.app.get(url)
        expected_url = "{}?next={}".format(settings.LOGIN_URL, url)
        self.assertRedirects(redirect, expected_url)

        edit_page = self.app.get(url, user=self.user)
        self.assertEqual(edit_page.status_code, 200)

    def test_edit_page(self):
        """ Test that the change password link is still present and form submission works """
        url = reverse('profile')
        edit_page = self.app.get(url, user=self.user)
        self.assertContains(edit_page, _('Change password'))

        fields = {
            'email': 'foo@bar.com',
            'first_name': 'Foo',
            'last_name': 'Bar',
            'userprofile_set-0-street': 'StraatFoobar'
        }

        form = edit_page.forms[0]
        for field, value in fields.items():
            form[field] = value
        result = form.submit().follow()
        self.assertContains(result, _('Your profile data has been updated.'))

        user = self.user.__class__.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, fields['email'])
        self.assertEqual(user.first_name, fields['first_name'])
        self.assertEqual(user.last_name, fields['last_name'])
        self.assertEqual(user.profile.street, fields['userprofile_set-0-street'])
