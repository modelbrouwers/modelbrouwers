from django.core import mail
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_webtest import WebTest

from ..models import User
from .factories import UserFactory


class UserApprovalTests(WebTest):
    signed_up_user: User

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.superuser = UserFactory.create(superuser=True)
        cls.signed_up_user = UserFactory.create(
            username="some-suspicious-user",
            email="not-a-spammer@example.com",
            ip_address_joined=None,  # we don't need the resolution in tests :)
            registration_motivation="I'm totally not going to spam.",
            approved_or_rejected_on=None,
            is_active=False,
        )
        cls.admin_url_approval = reverse(
            "admin:user_registration_approval",
            kwargs={"object_id": cls.signed_up_user.pk},
        )

    def test_non_privileged_staff_user_cant_access_view(self):
        staff_user = UserFactory.create(
            is_staff=True,
            superuser=False,
            permissions=["users.view_user", "users.add_user"],
        )
        self.app.set_user(staff_user)

        with self.subTest("GET page"):
            self.app.get(self.admin_url_approval, status=403)

        with self.subTest("POST to page"):
            self.app.post(self.admin_url_approval, status=403)

        # we allow the link to be in the page despite no permissions applying - this is
        # a nightmare in Django admin to apply permissions on objects in the change list

    def test_staff_user_with_privileges_has_link_in_list_page(self):
        staff_user = UserFactory.create(
            is_staff=True,
            superuser=False,
            permissions=["users.change_user", "users.add_user"],
        )
        self.app.set_user(staff_user)

        changelist_response = self.app.get(reverse("admin:users_user_changelist"))

        self.assertContains(changelist_response, self.admin_url_approval)

    def test_rejecting_approval_keeps_account_deactivated(self):
        self.app.set_user(self.superuser)
        approval_page = self.app.get(self.admin_url_approval)
        form = approval_page.forms["registration_approval_form"]

        assert "reject" in form.fields
        with self.captureOnCommitCallbacks(execute=True):
            response = form.submit(name="reject")

        self.assertEqual(response.status_code, 302)
        self.signed_up_user.refresh_from_db()
        self.assertFalse(self.signed_up_user.is_active)
        self.assertIsNotNone(self.signed_up_user.approved_or_rejected_on)
        self.assertFalse(self.signed_up_user.needs_registration_approval)

        with self.subTest("email notification sent"):
            self.assertEqual(len(mail.outbox), 1)
            message = mail.outbox[0]
            self.assertEqual(message.to, ["not-a-spammer@example.com"])

    def test_approving_activates_account(self):
        self.app.set_user(self.superuser)
        approval_page = self.app.get(self.admin_url_approval)
        form = approval_page.forms["registration_approval_form"]

        assert "approve" in form.fields
        with self.captureOnCommitCallbacks(execute=True):
            response = form.submit(name="approve")

        self.assertEqual(response.status_code, 302)
        self.signed_up_user.refresh_from_db()
        self.assertTrue(self.signed_up_user.is_active)
        self.assertIsNotNone(self.signed_up_user.approved_or_rejected_on)
        self.assertFalse(self.signed_up_user.needs_registration_approval)

        with self.subTest("email notification sent"):
            self.assertEqual(len(mail.outbox), 1)
            message = mail.outbox[0]
            self.assertEqual(message.to, ["not-a-spammer@example.com"])

    def test_user_cannot_be_approved_or_rejected_twice(self):
        now = timezone.now()
        self.signed_up_user.approved_or_rejected_on = now
        self.signed_up_user.save()
        self.app.set_user(self.superuser)

        approval_page = self.app.get(self.admin_url_approval)

        self.assertRedirects(
            approval_page,
            reverse(
                "admin:users_user_change", kwargs={"object_id": self.signed_up_user.pk}
            ),
        )
        self.signed_up_user.refresh_from_db()
        self.assertEqual(self.signed_up_user.approved_or_rejected_on, now)

    def test_staff_user_must_pick_approve_or_reject(self):
        self.app.set_user(self.superuser)
        approval_page = self.app.get(self.admin_url_approval)
        form = approval_page.forms["registration_approval_form"]

        response = form.submit(name="something else")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _("You must pick approve or reject."))
        self.signed_up_user.refresh_from_db()
        self.assertFalse(self.signed_up_user.is_active)
        self.assertIsNone(self.signed_up_user.approved_or_rejected_on)
        self.assertTrue(self.signed_up_user.needs_registration_approval)
