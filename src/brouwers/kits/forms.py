from django import forms

from .models import ModelKit


class ModelKitForm(forms.ModelForm):
    class Meta:
        model = ModelKit
        fields = ("name", "brand", "scale")
