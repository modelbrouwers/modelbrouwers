from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from brouwers.migration.models import UserMigration
from brouwers.forum_tools.models import ForumUser
from brouwers.awards.models import Project
from .models import UserProfile, RegistrationQuestion

User = get_user_model()


######################################
#  Registration and migration stuff  #
######################################
class UserProfileForm(UserCreationForm):
    forum_nickname = forms.CharField(required=True,min_length=3, max_length=20)
    exclude_from_nomination = forms.BooleanField(required=False)
    email = forms.EmailField(label=_("E-mail"), max_length=75, required=True)

    def clean_forum_nickname(self):
        nickname = self.cleaned_data['forum_nickname']
        try:
            UserProfile.objects.get(forum_nickname=nickname)
            raise forms.ValidationError(_("A user with that username already exists."))
            return nickname
        except UserProfile.DoesNotExist:
            return nickname

    def save(self, commit=False):
        user = super(UserProfileForm, self).save(commit=False)
        user.save()
        profile = UserProfile(user=user)
        profile.forum_nickname = self.cleaned_data['forum_nickname']
        if self.cleaned_data['exclude_from_nomination']:
            profile.exclude_from_nomination = True
        profile.save()
        return user

#TODO validate email, should be unique
class RegistrationForm(forms.ModelForm):
    """ Form to handle new registrations """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    forum_nickname = forms.CharField(required=True, min_length=3, max_length=30, label=_("Username"))
    email = forms.EmailField(required=True, label=_("E-mail address"))
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ('forum_nickname', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        users = User.objects.filter(email=email)
        if users:
            raise forms.ValidationError(_("This e-mail address is already registered."))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def clean_forum_nickname(self):
        msg = self.error_messages['duplicate_username']
        nickname = self.cleaned_data['forum_nickname']

        if UserMigration.objects.filter(username__iexact=nickname).exists():
            raise forms.ValidationError(msg)

        if UserProfile.objects.filter(forum_nickname__iexact=nickname).exists():
            raise forms.ValidationError(msg)

        username = nickname.replace(" ", "_")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(msg)
        return nickname

    def save(self, commit=True):
        forum_nickname = self.cleaned_data['forum_nickname']
        user = User(username=forum_nickname)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AnswerForm(forms.Form):
    answer = forms.CharField(label=_("answer"), required=True)


class QuestionForm(forms.Form):
    question = forms.ModelChoiceField(queryset=RegistrationQuestion.objects.filter(in_use=True), empty_label=None, widget=forms.HiddenInput())


class ForumAccountForm(forms.Form):
    """ Migrations """
    forum_nickname = forms.CharField(required=True, min_length=2, max_length=30, label=_("Forum name"))
    hash = forms.CharField(required=True, min_length=24, max_length=24, label=_("Code"))
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2

    def clean_forum_nickname(self):
        u = self.get_usermigration()
        if not u:
            raise forms.ValidationError(_("This user doesn't exist on the board, check for typos."))
        return self.cleaned_data['forum_nickname']

    def clean(self): #TODO: loggen foutieve ingaves
        user = self.get_usermigration()
        try:
            h = self.cleaned_data["hash"]
            if user.hash and h.lower() != user.hash.lower():
                raise forms.ValidationError(_("You entered the wrong code."))
                del self.cleaned_data["forum_nickname"]
                del self.cleaned_data["hash"]
        except KeyError: #hash was invalid
            pass
        return self.cleaned_data

    def get_usermigration(self):
        try:
            nickname = self.cleaned_data['forum_nickname']
            try:
                user = UserMigration.objects.get(username__exact=nickname)
            except UserMigration.DoesNotExist:
                user = None
        except KeyError: #forum_nickname not there
            raise forms.ValidationError(_("The username entered was not correct."))
        return user


######################################
#          Password resets           #
######################################
class RequestPasswordResetForm(forms.Form):
    forum_nickname = forms.CharField(
            required=False, min_length=2,
            max_length=30, label=_("Username")
            )
    email = forms.EmailField(
        required=False, label=_("E-mail address"),
        help_text=_("If you forgot your username, you can enter the e-mail address you registered with.")
        )

    def clean_forum_nickname(self):
        username = self.cleaned_data['forum_nickname']
        profiles = UserProfile.objects.filter(forum_nickname__iexact=username)
        if not profiles and username != '':
            raise forms.ValidationError(_("This user is unknown in the database."))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email__iexact=email)
        if not users and email != '':
            raise forms.ValidationError(_("This email adress is unknown in the database"))
        return email

    def clean(self):
        username = self.cleaned_data.get('forum_nickname', '')
        email = self.cleaned_data.get('email', '')
        if not email and not username:
            raise forms.ValidationError(_("Enter your username or e-mail address."))
        return self.cleaned_data

    def get_user(self):
        forum_nickname = self.cleaned_data['forum_nickname']
        if forum_nickname:
            user = User.objects.get(userprofile__forum_nickname__iexact=forum_nickname)
        else:
            email = self.cleaned_data['email']
            user = User.objects.get(email__iexact=email)
        return user


class HashForm(forms.Form):
    h = forms.CharField(required=True, min_length=24, max_length=24, widget=forms.HiddenInput)


class PasswordResetForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.HiddenInput
    )
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                _("The two password fields didn't match."))
        return password2


######################################
#            Profile stuff           #
######################################
class UserForm(forms.ModelForm):
    _original_email = None
    _profile = None

    class Meta:
        model = User
        fields =('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.TextInput(attrs={'size':30})
        }

    def __init__(self, profile=None, *args, **kwargs):
        user = kwargs['instance']
        self._original_email = user.email
        if profile:
            self._profile = profile
        super(UserForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self._original_email != self.cleaned_data['email']:
            new_email = self.cleaned_data['email']
            try:
                forum_user = ForumUser.objects.get(username=self._profile.forum_nickname)
                forum_user.user_email = new_email
                forum_user.save()
            except ForumUser.DoesNotExist: # user hasn't been on the forum yet, so no record exists
                pass
            finally:
                super(UserForm, self).save(*args, **kwargs)


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('street', 'number', 'postal', 'city', 'province', 'country')


class AwardsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('exclude_from_nomination',)

    def save(self, *args, **kwargs):
        profile = super(AwardsForm, self).save(*args, **kwargs)
        if profile.exclude_from_nomination:
            projects = Project.objects.filter(brouwer__iexact=profile.forum_nickname)
            for project in projects:
                project.rejected = True
                project.save()


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'last_vote', 'forum_nickname', 'secret_santa')


class SharingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('allow_sharing',)


######################################
#      Logging in from the board     #
######################################
class RedirectForm(forms.Form):
    redirect = forms.CharField(required=False, widget=forms.HiddenInput())
    next = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_redirect(self):
        path = self.cleaned_data.get('redirect')
        if path:
            return "%s%s" % (settings.PHPBB_URL, path[1:])
        return None

    def clean_next(self):
        path = self.cleaned_data.get('next')
        if path and not ' ' in path:
            return path
        return settings.LOGIN_REDIRECT_URL
