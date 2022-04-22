from django import forms
from django.conf import settings


class RedirectForm(forms.Form):
    redirect = forms.CharField(required=False, widget=forms.HiddenInput())
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_redirect(self):
        path = self.cleaned_data.get("redirect")
        if path:
            return "%s%s" % (settings.PHPBB_URL, path[1:])
        return None

    def clean_next(self):
        path = self.cleaned_data.get("next")
        if path and " " not in path:
            return path
        return settings.LOGIN_REDIRECT_URL
