from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Brand, KitDifficulties, Scale


class ModelKitForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    scale = forms.ModelChoiceField(queryset=Scale.objects.all())
    name = forms.CharField(required=False)


class AddKitForm(forms.Form):
    brand = forms.CharField(label=_('brand'))
    scale = forms.CharField(label=_('scale'))
    name = forms.CharField(label=_('name'))

    kit_number = forms.CharField(label=_('kit number'))
    box_image = forms.ImageField(label=_('box image'))
    difficulty = forms.ChoiceField(
        label=_('difficulty'), choices=KitDifficulties.choices,
        widget=forms.RadioSelect
    )


class ModelKitSelect(forms.SelectMultiple):
    """
    Subclassed to be more explicit and inject subforms for sniplates.
    """
    def __init__(self, *args, **kwargs):
        super(ModelKitSelect, self).__init__(*args, **kwargs)
        self.form = ModelKitForm(prefix='__modelkitselect')
        self.add_form = AddKitForm(prefix='__modelkitadd')
