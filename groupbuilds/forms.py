from django import forms

from .models import GroupBuild


class GroupBuildForm(forms.ModelForm):
    class Meta:
        model = GroupBuild
        fields = ('theme', 'category', 'description', 'admins',
                  'start', 'duration', 'rules', 'rules_topic_id',
                  'homepage_topic_id', 'introduction_topic_id')
