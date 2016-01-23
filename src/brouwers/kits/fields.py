from django.db import models
from django import forms

from .widgets import ModelKitSelect


class KitsManyToManyField(models.ManyToManyField):

    def __init__(self, *args, **kwargs):
        super(KitsManyToManyField, self).__init__('kits.ModelKit', *args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.setdefault('widget', ModelKitSelect)
        kwargs.setdefault('form_class', MultipleKitChoiceField)
        formfield = super(KitsManyToManyField, self).formfield(**kwargs)
        return formfield


class MultipleKitChoiceField(forms.ModelMultipleChoiceField):
    pass
