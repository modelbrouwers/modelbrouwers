from urllib.parse import parse_qs, urlparse

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms.fields import IntegerField
from django.utils.translation import gettext_lazy as _

from .widgets import ForumToolsIDFieldWidget

__all__ = ["ForumIDField", "TopicIDField"]


class IDField(IntegerField):
    default_error_messages = {
        "invalid_url": _("Enter a valid url"),
    }
    urlparam = None
    widget = ForumToolsIDFieldWidget

    def __init__(self, *args, **kwargs):
        if not kwargs.get("widget"):
            kwargs["widget"] = ForumToolsIDFieldWidget(
                urlparam=self.urlparam, type_=self.type_
            )
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        try:  # check if it's integer or not
            return super().to_python(value)
        except ValidationError:  # catch errors and check for urls
            pass

        # trigger URL validation
        try:
            URLValidator()(value)
        except ValidationError as e:
            e.code = "invalid_url"
            raise

        # start processing it as an url
        url = urlparse(value)
        querydict = parse_qs(url.query)
        _id = querydict.get(self.urlparam, None)
        if _id is None:
            raise ValidationError(self.error_messages["invalid_url"])
        return int(_id[0])  # is a list


class ForumIDField(IDField):
    type_ = "forum"

    def __init__(self, urlparam="f", *args, **kwargs):
        self.urlparam = urlparam
        super().__init__(*args, **kwargs)


class TopicIDField(IDField):
    type_ = "topic"

    def __init__(self, urlparam="t", *args, **kwargs):
        self.urlparam = urlparam
        super().__init__(*args, **kwargs)
