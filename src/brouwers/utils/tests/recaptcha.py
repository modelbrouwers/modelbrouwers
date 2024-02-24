from unittest.mock import patch

from django_recaptcha.client import RecaptchaResponse


def mock_recaptcha(is_valid: bool = True, action=None):
    patcher = patch(
        "django_recaptcha.fields.client.submit",
        return_value=RecaptchaResponse(is_valid=is_valid, action=action),
    )
    return patcher
