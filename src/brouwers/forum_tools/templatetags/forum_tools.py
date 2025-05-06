from django import template

register = template.Library()


@register.filter("idfield_url")
def idfield_url(widget, value):
    return widget.get_url(value)
