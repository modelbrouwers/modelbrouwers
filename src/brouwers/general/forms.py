from django import forms
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme


class RedirectForm(forms.Form):
    redirect = forms.CharField(required=False, widget=forms.HiddenInput())
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def _check_allowed_host_and_scheme(self, url: str):
        return url_has_allowed_host_and_scheme(
            url=url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        )

    def clean_redirect(self):
        path = self.cleaned_data.get("redirect")
        if path and self._check_allowed_host_and_scheme(path):
            return "%s%s" % (settings.PHPBB_URL, path[1:])
        return None

    def clean_next(self):
        next_url = self.cleaned_data.get("next")
        if next_url and self._check_allowed_host_and_scheme(next_url):
            return next_url
        return settings.LOGIN_REDIRECT_URL
