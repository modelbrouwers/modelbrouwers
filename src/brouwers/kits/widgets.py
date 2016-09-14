from django import forms
from django.urls import reverse_lazy
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
    box_image = forms.ImageField(label=_('box image'), widget=forms.FileInput(attrs={
        'data-endpoint': reverse_lazy('api:boxart-list')
    }))
    difficulty = forms.ChoiceField(
        label=_('difficulty'), choices=KitDifficulties.choices,
        widget=forms.RadioSelect
    )


class ModelKitSelectMixin(object):
    """
    Mixin that injects subforms into sniplates widgets.
    """

    def __init__(self, *args, **kwargs):
        super(ModelKitSelectMixin, self).__init__(*args, **kwargs)
        self.form = ModelKitForm(prefix='__modelkitselect')
        self.add_form = AddKitForm(prefix='__modelkitadd')


class ModelKitSelect(ModelKitSelectMixin, forms.Select):
    pass


class ModelKitSelectMultiple(ModelKitSelectMixin, forms.SelectMultiple):
    pass
