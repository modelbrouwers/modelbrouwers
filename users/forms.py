from django import forms
from django.utils.translation import ugettext_lazy as _

from general.models import RegistrationQuestion
from .models import User


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    question = forms.ModelChoiceField(queryset=RegistrationQuestion.active.all(), empty_label=None)
    answer = forms.CharField(label=_('Answer'), max_length=255)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        question = cleaned_data.get('question')
        answer = cleaned_data.get('answer')
        if question and answer:
            valid_answer = question.answers.filter(answer__iexact=answer).exists()
            if not valid_answer:
                del cleaned_data['answer']
                msg = _('Invalid answer. Make sure to read the entire question!')
                self._errors['answer'] = self.error_class([msg])
                raise forms.ValidationError(_('You provided an incorrect answer to the anti-bot question.'))

        return cleaned_data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
