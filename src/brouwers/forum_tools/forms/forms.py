from django import forms
from django.utils.translation import ugettext_lazy as _

from brouwers.general.utils import clean_username as _clean_username
from ..models import Forum, ForumUser


__all__ = ['ForumForm', 'PosterIDsForm', 'ForumUserForm']


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


class ForumUserForm(forms.Form):
    username = forms.CharField(max_length=254)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password."),
    }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return _clean_username(username)

    def get_user(self):
        """ Query the database for the user. """
        try:
            return ForumUser.objects.get(username_clean=self.cleaned_data['username'])
        except ForumUser.DoesNotExist:
            return None
