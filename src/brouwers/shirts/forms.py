from django import forms
from models import ShirtOrder

class ShirtOrderForm(forms.ModelForm):
    class Meta:
        model = ShirtOrder
        fields = ('size', 'type', 'color', 'send_per_mail', 'moderator')
