from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Brand, Scale


class ModelKitForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    scale = forms.ModelChoiceField(queryset=Scale.objects.all())
    name = forms.CharField(required=False)


class AddKitForm(forms.Form):
    brand = forms.CharField(label=_('brand'))
    scale = forms.CharField(label=_('scale'))
    name = forms.CharField(label=_('name'))


class ModelKitSelect(forms.TextInput):
    """
    Subclassed to be more explicit and allow comma separated values.

    Very roughly based on `django.contrib.admin.widgets.ManyToManyRawIdWidget`.
    """
    def __init__(self, *args, **kwargs):
        super(ModelKitSelect, self).__init__(*args, **kwargs)
        self.form = ModelKitForm(prefix='__modelkitselect')
        self.add_form = AddKitForm(prefix='__modelkitadd')

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(',')
