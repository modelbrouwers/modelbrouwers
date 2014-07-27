import urllib

from django import forms
from django.conf import settings
from django.contrib.sites.models import Site
from django.forms.widgets import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html, smart_urlquote
from django.utils.translation import ugettext as _


class ForumToolsIDFieldWidget(forms.TextInput):
    def __init__(self, urlparam=None, type_=None, **kwargs):
        assert urlparam is not None
        assert type_ in ['topic', 'forum'] # viewtopic.php, viewforum.php
        self.urlparam = urlparam
        self.type_ = type_
        super(ForumToolsIDFieldWidget, self).__init__(**kwargs)

    def render(self, name, value, attrs=None):
        if value:
            value = self.get_url(value)
        html = super(ForumToolsIDFieldWidget, self).render(name, value, attrs)
        if value:
            value = force_text(value)
            final_attrs = {'href': smart_urlquote(value)}
            html = format_html(
                '<p class="url">{0} <a{1}>{2}</a><br />{3} {4}</p>',
                _('Currently:'), flatatt(final_attrs), value,
                _('Change:'), html
            )
        return html

    def get_url(self, value):
        if not value:
            return None
        return '{scheme}://{domain}{prefix}/view{type}.php?{qs}'.format(
            scheme='http',
            domain=Site.objects.get_current().domain,
            prefix=settings.PHPBB_URL,
            type=self.type_,
            qs=urllib.urlencode({self.urlparam: value})
        )
