from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

import requests_mock
from requests.exceptions import ConnectionError

from ..validators import validate_image_url


@requests_mock.Mocker()
class ImageURLValidatorTests(SimpleTestCase):
    def test_valid_image(self, m):
        image_urls = (
            ("https://example.com/image.jpg", "image/jpg"),
            ("https://example.com/image.png", "image/png"),
            ("http://dummy/foo/", "image/gif"),
        )
        for url, ct in image_urls:
            with self.subTest(url=url, content_type=ct):
                m.head(url, headers={"Content-Type": ct})

                try:
                    validate_image_url(url)
                except ValidationError:
                    self.fail("Should have passed")

    def test_connection_error(self, m):
        m.head("https://example.com/image.jpg", exc=ConnectionError)

        with self.assertRaises(ValidationError):
            validate_image_url("https://example.com/image.jpg")

    def test_bad_response_status_code(self, m):
        m.head("https://example.com/image.jpg", status_code=400)

        with self.assertRaises(ValidationError):
            validate_image_url("https://example.com/image.jpg")

    def test_not_an_image_according_to_headers(self, m):
        m.head("https://example.com/", headers={"Content-Type": "text/html"})

        with self.assertRaises(ValidationError):
            validate_image_url("https://example.com/")
