from django import forms
from django.utils.translation import ugettext as _
from models import Forum

class ForumForm(forms.Form):
    forum = forms.ModelChoiceField(queryset=Forum.objects.all(), empty_label=None)

class PosterIDsForm(forms.Form):
    poster_ids = forms.CharField()

    def clean_poster_ids(self):
        poster_ids = self.cleaned_data['poster_ids']
        list_ids = poster_ids.split(',')
        try:
            poster_ids = [int(_id) for _id in list_ids]
            self.poster_ids = poster_ids
        except ValueError:
            raise forms.ValidationError(_('Provide a set of IDS separated by \';\''))
        return poster_ids