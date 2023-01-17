from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

import requests


class ImageURLValidator:
    message = _("Enter a valid image URL.")
    code = "invalid_image_url"

    def __call__(self, value: str):
        try:
            response = requests.head(value, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise ValidationError(
                self.message, code=self.code, params={"value": value}
            ) from exc

        response_ct = response.headers.get("Content-Type", "application/octet-stream")
        content_type = response_ct.split(";", 1)[0].lower()
        if not content_type.startswith("image/"):
            raise ValidationError(self.message, code=self.code, params={"value": value})


validate_image_url = ImageURLValidator()
