from django import forms
from models import Participant

class EnrollForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('secret_santa', 'user')
        widgets = {
            'secret_santa': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }
