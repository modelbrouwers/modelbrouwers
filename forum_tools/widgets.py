from urlparse import urlparse, parse_qs

from django.forms.widgets import TextInput


class IDWidget(TextInput):
    urlparam = None # to be set by inherited class

    def value_from_datadict(self, data, files, name):
        """
        Given a dictionary of data and this widget's name, returns the value
        of this widget. Returns None if it's not provided.

        The entered data can be an url or ID.
        """
        value = data.get(name, None)
        if value is not None:
            try:
                url = urlparse(value)
            except AttributeError: # not a string
                pass
            else:
                querydict = parse_qs(url.query)
                ids = querydict.get(self.urlparam, None)
                if ids is not None:
                    value = ids[0]
        return value


class ForumIDWidget(IDWidget):
    def __init__(self, urlparam='f', *args, **kwargs):
        self.urlparam = urlparam
        super(ForumIDWidget, self).__init__(*args, **kwargs)


class TopicIDWidget(IDWidget):
    def __init__(self, urlparam='t', *args, **kwargs):
        self.urlparam = urlparam
        super(TopicIDWidget, self).__init__(*args, **kwargs)
