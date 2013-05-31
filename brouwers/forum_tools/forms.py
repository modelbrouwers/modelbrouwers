from django import forms
from models import Forum

class ForumForm(forms.Form):
    forum = forms.ModelChoiceField(queryset=Forum.objects.all(), empty_label=None)