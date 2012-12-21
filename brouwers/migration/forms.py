from django import forms
from django.conf import settings
from models import PhotoMigration

class PhotoMigrationForm(forms.Form):
    start = forms.IntegerField(min_value=0, initial=0)
    end = forms.IntegerField(min_value=0, initial=2000)
