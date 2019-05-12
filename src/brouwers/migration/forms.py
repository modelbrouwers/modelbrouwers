from django import forms


class PhotoMigrationForm(forms.Form):
    start = forms.IntegerField(min_value=0, initial=0)
    end = forms.IntegerField(min_value=0, initial=2000)
