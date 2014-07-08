from django import forms

from .models import GroupBuild


class GroupBuildForm(forms.ModelForm):
    class Meta:
        model = GroupBuild
        fields = ('theme',)
