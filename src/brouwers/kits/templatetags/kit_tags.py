from __future__ import division

from django.template import Library

register = Library()


@register.inclusion_tag('kits/includes/kit_tags.html')
def kit_tags(form=None, data=None):
    return {
        'add_form': form,
        'data': data
    }
