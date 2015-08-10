from django import forms

from .models import Brand, Scale


class ModelKitForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all())
    scale = forms.ModelChoiceField(queryset=Scale.objects.all())


class ModelKitSelect(forms.TextInput):
    """
    Subclassed to be more explicit and allow comma separated values.

    Very roughly based on `django.contrib.admin.widgets.ManyToManyRawIdWidget`.
    """
    def __init__(self, *args, **kwargs):
        super(ModelKitSelect, self).__init__(*args, **kwargs)
        self.form = ModelKitForm(prefix='__modelkitselect')

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(',')
