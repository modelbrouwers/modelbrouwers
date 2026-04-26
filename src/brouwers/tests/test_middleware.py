from django.http import HttpRequest, HttpResponse
from django.test import TestCase, override_settings
from django.urls import include, path
from django.utils import translation

from brouwers.users.tests.factories import UserFactory


def echo_active_language(request: HttpRequest):
    language = translation.get_language()
    return HttpResponse(language)


urlpatterns = [
    path("lang/", echo_active_language),
    path("", include("brouwers.users.urls", namespace="users")),
]


@override_settings(ROOT_URLCONF=__name__)
class UILanguageMiddlewareTests(TestCase):
    def test_anon_user_accept_header_used(self):
        language_codes = (
            ("en", b"en"),
            ("nl", b"nl"),
            ("nl-BE", b"nl"),
        )

        for requested_language_code, expected in language_codes:
            with self.subTest(
                requested_language_code=requested_language_code, expected=expected
            ):
                response = self.client.get(
                    "/lang/", headers={"Accept-Language": requested_language_code}
                )

                self.assertEqual(response.content, expected)

    def test_authenticated_user_without_preference_set(self):
        user = UserFactory.create()
        assert user.ui_language == ""
        self.client.force_login(user=user)

        response = self.client.get("/lang/", headers={"Accept-Language": "nl-NL"})

        self.assertEqual(response.content, b"nl")

    def test_authenticated_user_with_preference_set(self):
        user = UserFactory.create(ui_language="en")
        self.client.force_login(user=user)

        response = self.client.get("/lang/", headers={"Accept-Language": "nl-NL"})

        self.assertEqual(response.content, b"en")
