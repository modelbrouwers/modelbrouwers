import base64
from typing import cast
from unittest.mock import patch

from django.test import SimpleTestCase

import requests_mock

from ..client import Client
from .utils import patch_cache, patch_config


class ClientTests(SimpleTestCase):
    @patch_cache(
        {
            "token": {"expires_in": 3600, "access_token": "brouwers-dummy"},
        }
    )
    @patch("brouwers.shop.payments.paypal.client.OAuth2Session.close")
    def test_client_basic_usage(self, mock_close):
        client = Client()

        with self.subTest("client session not accessed (lazy)"):
            with client:
                pass
            mock_close.assert_not_called()

        with self.subTest("client session accessed"):
            with client:
                client.session
            mock_close.assert_called_once()

    @patch_cache(backend="django.core.cache.backends.locmem.LocMemCache")
    @requests_mock.Mocker()
    @patch_config()
    def test_gets_access_token_from_config(self, m, mock_get_solo):
        # taken from https://developer.paypal.com/api/rest/authentication/
        m.post(
            "https://api-m.paypal.com/v1/oauth2/token",
            json={
                "scope": "removed because irrelevant",
                "access_token": "mock-token",
                "token_type": "Bearer",
                "app_id": "APP-mock",
                "expires_in": 60,
                "nonce": "mock-nonce",
            },
        )
        client = Client()
        self.addCleanup(client.cache.clear)

        token = cast(dict, client.session.token)

        self.assertIsNotNone(token)
        self.assertEqual(token["access_token"], "mock-token")
        self.assertEqual(token["token_type"], "Bearer")

        self.assertEqual(len(m.request_history), 1)
        token_request = m.last_request
        self.assertEqual(token_request.body, "grant_type=client_credentials")
        auth_header = token_request.headers["Authorization"]
        auth_type, value = auth_header.split(" ")
        self.assertEqual(auth_type, "Basic")
        self.assertEqual(
            base64.b64decode(value),
            b"dummy-client-id:dummy-client-secret",
        )

        with self.subTest("Check that token is re-used from cache"):
            other_client = Client()

            same_token = cast(dict, other_client.session.token)

            self.assertEqual(same_token, token)
            self.assertEqual(len(m.request_history), 1)
