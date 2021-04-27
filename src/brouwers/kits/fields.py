from django import forms
from django.db import models

from .widgets import ModelKitSelect, ModelKitSelectMultiple


class KitForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        to = kwargs.pop("to", "kits.ModelKit")
        super().__init__(to, *args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.setdefault("widget", ModelKitSelect)
        kwargs.setdefault("form_class", KitChoiceField)
        return super().formfield(**kwargs)


class KitsManyToManyField(models.ManyToManyField):
    def __init__(self, *args, **kwargs):
        # to is in kwargs during reconstruct
        to = kwargs.pop("to", "kits.ModelKit")
        super().__init__(to, *args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.setdefault("widget", ModelKitSelectMultiple)
        kwargs.setdefault("form_class", MultipleKitChoiceField)
        return super().formfield(**kwargs)


class KitChoiceField(forms.ModelChoiceField):
    pass


class MultipleKitChoiceField(forms.ModelMultipleChoiceField):
    pass
