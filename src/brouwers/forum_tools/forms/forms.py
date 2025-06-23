from django import forms
from django.utils.translation import gettext_lazy as _

from brouwers.general.utils import clean_username as _clean_username

from ..models import Forum, ForumUser

__all__ = ["ForumForm", "ForumUserForm"]


class ForumForm(forms.Form):
    forum = forms.ModelChoiceField(queryset=Forum.objects.all(), empty_label=None)


class ForumUserForm(forms.Form):
    username = forms.CharField(max_length=254)

    error_messages = {
        "invalid_login": _("Please enter a correct username and password."),
    }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        return _clean_username(username)

    def get_user(self):
        """Query the database for the user."""
        try:
            return ForumUser.objects.get(username_clean=self.cleaned_data["username"])
        except ForumUser.DoesNotExist:
            return None
