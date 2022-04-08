from datetime import date, timedelta

from django.conf import settings
from django.urls import reverse

from django_webtest import WebTest

from brouwers.users.tests.factories import UserFactory

from ..models import GroupbuildStatuses, Participant
from .factories import GroupBuildFactory, ParticipantFactory


class ViewTests(WebTest):
    def test_detail_page(self):
        gb = GroupBuildFactory.create()
        gb.admins.add(gb.applicant)
        url = gb.get_absolute_url()

        # anonymous user
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(gb.theme, response)
        self.assertFalse(response.context["can_edit"])

        # login as owner user
        response = self.app.get(url, user=gb.applicant)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["can_edit"])

        # and as superuser
        superuser = UserFactory.create(is_staff=True, is_superuser=True)
        response = self.app.get(url, user=superuser)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["can_edit"])

    def test_user_participant(self):
        """Test that an authenticated user can edit his participant details"""

        gb = GroupBuildFactory.create()
        ps = ParticipantFactory.create_batch(3, groupbuild=gb)

        self.assertIsNone(gb.end)
        self.assertEqual(gb.participant_set.count(), 3)

        edit_urls = [
            reverse(
                "groupbuilds:update-participant", kwargs={"slug": gb.slug, "pk": p.pk}
            )
            for p in ps
        ]
        response = self.app.get(gb.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        for url in edit_urls:
            self.assertNotIn(url, response)

        # now as an authenticated user
        user = ps[0].user
        url = reverse(
            "groupbuilds:update-participant", kwargs={"slug": gb.slug, "pk": ps[0].pk}
        )
        p_form = self.app.get(url, user=user)
        self.assertEqual(p_form.status_code, 200)
        self.assertTemplateUsed(p_form, "groupbuilds/participant_form.html")
        self.assertTemplateUsed(p_form, "groupbuilds/includes/progress.html")
        self.assertTemplateUsed(p_form, "groupbuilds/includes/links.html")
        self.assertEqual(p_form.context["gb"], gb)

        # alter the form
        p_form.form["model_name"] = "My updated model"
        p_form.form["topic"] = "http://modelbrouwers.nl/phpBB3/viewtopic.php?t=1"
        response = p_form.form.submit()
        self.assertRedirects(response, gb.get_absolute_url())

        # check that the data is effectively saved
        p = Participant.objects.get(pk=ps[0].pk)
        self.assertEqual(p.model_name, "My updated model")
        self.assertEqual(p.topic_id, 1)

        # user trying to edit a participant that is not himself
        self.assertNotEqual(ps[1].user, ps[0].user)
        p_form = self.app.get(url, user=ps[1].user, status=404)

        # test that groupbuilds that are past the end date can no longer be edited
        gb.end = date.today() - timedelta(days=1)
        gb.save()
        p_form = self.app.get(url, user=user, status=404)

    def test_dashboard(self):
        """Test that the correct groupbuilds are visible in the dashboard"""
        url = reverse("groupbuilds:dashboard")

        user = UserFactory.create()
        gb = GroupBuildFactory.create(
            applicant=user,
            status=GroupbuildStatuses.concept,
            reason_denied="My valid reason",
        )
        gb.admins.add(user)

        participant = ParticipantFactory.create(
            user=user, groupbuild__status=GroupbuildStatuses.accepted
        )

        dashboard = self.app.get(url)
        self.assertRedirects(dashboard, settings.LOGIN_URL + "?next={}".format(url))

        dashboard = self.app.get(url, user=user)
        self.assertEqual(dashboard.status_code, 200)
        qs = dashboard.context["view"].get_queryset()
        self.assertQuerysetEqual(
            qs, [repr(gb), repr(participant.groupbuild)], ordered=False
        )
