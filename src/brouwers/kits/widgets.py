from django import forms
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from .models import KitDifficulties


class AddKitForm(forms.Form):
    brand = forms.CharField(label=_("brand"))
    scale = forms.CharField(label=_("scale"))
    name = forms.CharField(label=_("name"))

    kit_number = forms.CharField(label=_("kit number"))
    box_image = forms.ImageField(
        label=_("box image"),
        widget=forms.FileInput(
            attrs={"data-endpoint": reverse_lazy("api:boxart-list")}
        ),
    )
    difficulty = forms.ChoiceField(
        label=_("difficulty"), choices=KitDifficulties.choices, widget=forms.RadioSelect
    )


class ModelKitSelectMixin(object):
    """
    Mixin that injects subforms into sniplates widgets.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_form = AddKitForm(prefix="__modelkitadd")


class ModelKitSelect(ModelKitSelectMixin, forms.Select):
    pass


class ModelKitSelectMultiple(ModelKitSelectMixin, forms.SelectMultiple):
    pass
