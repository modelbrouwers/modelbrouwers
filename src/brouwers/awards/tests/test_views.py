from django.conf import settings
from django.urls import reverse

from django_webtest import WebTest
from freezegun import freeze_time

from brouwers.users.tests.factories import UserFactory


class ViewTests(WebTest):
    def setUp(self):
        self.user = UserFactory.create()

    def test_login_required(self):
        index = self.app.get(reverse("voting"))
        login_url = "{0}?next={1}".format(settings.LOGIN_URL, reverse("voting"))
        self.assertRedirects(index, login_url)

    @freeze_time("2014-11-09")
    def test_voting_disabled(self):
        # voting should be disabled
        index = self.app.get(reverse("voting"), user=self.user)
        self.assertRedirects(index, reverse("awards_index"))
