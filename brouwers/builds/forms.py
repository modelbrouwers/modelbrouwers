from django import forms

class BrouwerSearchForm(forms.Form):
	nickname = forms.CharField(max_length=20)
