from rest_framework import fields
from sorl.thumbnail import get_thumbnail


class ThumbnailField(fields.ImageField):

    def __init__(self, dimensions, opts=None, *args, **kwargs):
        self.dimensions = dimensions
        self.opts = opts or {}
        super(ThumbnailField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        thumbs = {}
        request = self.context.get('request', None)
        for name, dim in self.dimensions:
            if not value:
                thumbs['%s' % name] = None
                continue

            image = get_thumbnail(value, dim, **self.opts)
            if request is not None:
                img_url = request.build_absolute_uri(image.url)
            else:
                img_url = super(ThumbnailField, self).to_representation(image.url)
            thumbs['%s' % name] = img_url

        return thumbs
