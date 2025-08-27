import logging

from rest_framework import fields
from sorl.thumbnail import get_thumbnail

logger = logging.getLogger(__name__)


class ThumbnailField(fields.ImageField):
    def __init__(self, dimensions, opts=None, *args, **kwargs):
        self.dimensions = dimensions
        self.opts = opts or {}
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        thumbs = {}
        request = self.context.get("request", None)
        for name, dim in self.dimensions:
            if not value:
                thumbs[f"{name}"] = None
                continue

            try:
                image = get_thumbnail(value, dim, **self.opts)
            except OSError:
                logger.exception("Could not create thumb/scaled version.")
                continue
            if request is not None:
                img_url = request.build_absolute_uri(image.url)
            else:
                img_url = super().to_representation(image.url)
            thumbs[f"{name}"] = img_url

        return thumbs
