from __future__ import division

from django.template import Library

register = Library()


@register.inclusion_tag('kits/includes/add_kit_modal.html')
def add_kit_modal(form):
    print('got form', form)
    return {

    }
