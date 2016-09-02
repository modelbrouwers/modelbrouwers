from __future__ import division

from django.template import Library

from ..widgets import AddKitForm

register = Library()


@register.inclusion_tag('kits/includes/add_kit_modal.html')
def add_kit_modal(form=None, data=None):
    if form is None:
        form = AddKitForm(prefix='__modelkitadd')
    return {
        'add_form': form,
        'data': data
    }
