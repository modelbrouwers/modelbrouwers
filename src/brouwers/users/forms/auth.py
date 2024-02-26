from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm as _PasswordResetForm,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from brouwers.forum_tools.models import ForumUser
from brouwers.general.utils import clean_username

from ..models import User


class AdminUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        "duplicate_username": _("A user with that username already exists."),
        "password_mismatch": _("The two password fields didn't match."),
        "duplicate_email": _("This e-mail address is already in use."),
    }
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User._default_manager.filter(email__iexact=email).exists():
            raise forms.ValidationError(self.error_messages["duplicate_email"])
        return email

    def clean_username(self):
        """
        user.username is unique on db level, BUT not on a case-insensitive base.
        """
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username__iexact=username)
        except User.DoesNotExist:
            try:
                # check ForumUsers that haven't migrated!
                ForumUser.objects.get(username_clean=clean_username(username))
            except ForumUser.DoesNotExist:
                return username
        raise forms.ValidationError(self.error_messages["duplicate_username"])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(self.error_messages["password_mismatch"])
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserCreationForm(AdminUserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3(action="signup"))
    accept_terms = forms.BooleanField(
        label=_("I have read and accepted the registration terms"), required=True
    )

    class Meta:
        model = User
        fields = ("username", "email")


class AuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Username or email")
        del self.fields["username"].widget.attrs["maxlength"]


class PasswordResetForm(_PasswordResetForm):
    username = forms.CharField(label=_("Username"), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = False

    def get_queryset(self, cleaned_data):
        UserModel = get_user_model()
        email, username = cleaned_data.get("email"), cleaned_data.get("username")
        query = {}
        if email:
            query["email__iexact"] = email
        if username:
            query["username__iexact"] = username
        return UserModel._default_manager.filter(**query)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("username") and not cleaned_data.get("email"):
            raise forms.ValidationError(_("Fill at least one field."))
        if not self.get_queryset(cleaned_data).exists():
            raise forms.ValidationError(_("We couldn't find a matching user."))
        return cleaned_data

    def save(self, **kwargs):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        request = kwargs.get("request")
        token_generator = kwargs.get("token_generator")
        use_https = kwargs.get("use_https")
        subject_template_name = kwargs.get("subject_template_name")
        email_template_name = kwargs.get("email_template_name")

        # retrieve the relevant user, username and email should be unique
        users = self.get_queryset(self.cleaned_data)
        if users.count() > 1:
            messages.warning(
                request,
                _(
                    "Multiple accounts were found, this shouldn't happen. "
                    "Please contact the admins (see e-mail in the page footer)."
                ),
            )
            return

        user = users.get()
        if not user.is_active:
            messages.warning(
                request,
                _(
                    "Your account is still inactive! You won't be able to "
                    "log in until you reactivate with the link sent by e-mail. "
                    "Check your spamfolder to see if you missed an e-mail."
                ),
            )
            return

        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain
        c = {
            "email": user.email,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
        }
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, None, [user.email])
        messages.success(
            request, _("An e-mail was sent with a link to reset your password.")
        )
