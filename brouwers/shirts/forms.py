from django import forms
from models import ShirtOrder

class ShirtOrderForm(forms.ModelForm):
    class Meta:
        model = ShirtOrder
        fields = ('size', 'type', 'color', 'send_per_mail', 'moderator')
    
    #def __init__(self, user, *args, **kwargs):
    #    super(ShirtOrderForm, self).__init__(*args, **kwargs)
