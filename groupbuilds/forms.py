from django import forms

from .models import GroupBuild


class GroupBuildForm(forms.ModelForm):
    class Meta:
        model = GroupBuild
        fields = ('theme', 'category', 'description', 'admins',
                  'start', 'duration', 'rules', 'rules_topic',
                  'homepage_topic', 'introduction_topic')

    def __init__(self, request, *args, **kwargs):
        super(GroupBuildForm, self).__init__(*args, **kwargs)
        if not self.instance.applicant_id:
            self.instance.applicant = request.user

    def save(self, *args, **kwargs):
        _created = self.instance.id is None and kwargs.get('commit', True)
        gb = super(GroupBuildForm, self).save(*args, **kwargs)
        if _created and gb.applicant not in gb.admins.all():
            gb.admins.add(gb.applicant)
        return gb


class DateForm(forms.Form):
    date = forms.DateField(required=False)

    def get_date(self):
        if self.is_valid():
            return self.cleaned_data['date']
        return None
