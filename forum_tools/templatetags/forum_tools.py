from django import template
from django.template.defaultfilters import stringfilter
from general.utils import get_forumname_for_username

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def forum_name(value):
    """ Translates username to forumname """
    return get_forumname_for_username(value)


@register.filter('idfield_url')
def idfield_url(widget, value):
    return widget.get_url(value)