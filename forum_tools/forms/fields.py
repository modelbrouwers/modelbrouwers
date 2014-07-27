import urlparse

from django.core.exceptions import ValidationError
from django.forms.fields import IntegerField
from django.utils.translation import ugettext_lazy as _


class IDField(IntegerField):
    default_error_messages = {
        'invalid_url': _('Enter a valid url'),
    }
    urlparam = None

    def to_python(self, value):
        try: # check if it's integer or not
            return super(IDField, self).to_python(value)
        except ValidationError: # catch errors and check for urls
            pass

        # start processing it as an url
        url = urlparse.urlparse(value)
        querydict = urlparse.parse_qs(url.query)
        _id = querydict.get(self.urlparam, None)
        if _id is None:
            raise ValidationError(self.error_messages['invalid_url'])
        return int(_id[0]) # is a list


class ForumIDField(IDField):
    def __init__(self, urlparam='f', *args, **kwargs):
        self.urlparam = urlparam
        super(ForumIDField, self).__init__(*args, **kwargs)


class TopicIDField(IDField):
    def __init__(self, urlparam='t', *args, **kwargs):
        self.urlparam = urlparam
        super(TopicIDField, self).__init__(*args, **kwargs)
