from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from brouwers.migration.models import UserMigration
from models import UserProfile, RegistrationQuestion

from django.utils.translation import ugettext_lazy as _

class UserProfileForm(UserCreationForm):
    forum_nickname = forms.CharField(required=True,min_length=3, max_length=20)
    exclude_from_nomination = forms.BooleanField(required=False)
    email = forms.EmailField(label=_("E-mail"), max_length=75, required=True)
    
    def clean_forum_nickname(self):
        nickname = self.cleaned_data['forum_nickname']
        try:
            UserProfile.objects.get(forum_nickname=nickname)
            raise forms.ValidationError(_("Deze forumnickname is al in gebruik bij een andere user op deze website."))
            return nickname
        except UserProfile.DoesNotExist:
            return nickname
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        #self.fields['username'].required = False
    
    #def clean(self):
    #    
    
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
        msg = _("This username has been taken.")
        nickname = self.cleaned_data['forum_nickname']
        try:
            migration_user = UserMigration.objects.get(username__iexact=nickname)
            raise forms.ValidationError(msg)
        except UserMigration.DoesNotExist:
            pass
        try:
            UserProfile.objects.get(forum_nickname__iexact=nickname)
            raise forms.ValidationError(msg)
            return nickname
        except UserProfile.DoesNotExist:
            return nickname
    
    def save(self, commit=True):
        forum_nickname = self.cleaned_data['forum_nickname']
        username = forum_nickname.replace(" ", "_")
        user = User(username=username)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            profile = UserProfile(user=user)
            profile.forum_nickname = forum_nickname
            profile.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username = username.replace(" ", "_")
        return username

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'last_vote', 'forum_nickname')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =('email', 'first_name', 'last_name')
        widgets = {
            'email': forms.TextInput(attrs={'size':30})
        }

class ForumAccountForm(forms.Form):
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
            raise forms.ValidationError(_("Deze gebruiker bestaat niet op het forum. Controleer op typfouten."))
        #try:
        #    username = u.username.replace(' ', '_')
        #    user = User.objects.get(username=username)
        #except User.DoesNotExist:
        #    raise forms.ValidationError("Je bent aan het foefelen... dit wordt gelogd!")
        return self.cleaned_data['forum_nickname']
    
    def clean(self): #TODO: loggen foutieve ingaves
        user = self.get_usermigration()
        try:
            h = self.cleaned_data["hash"]
            if h.lower() != user.hash.lower():
                raise forms.ValidationError(_("Je hebt een foutieve code ingegeven."))
                del self.cleaned_data["forum_nickname"]
                del self.cleaned_data["hash"]
        except KeyError: #has was invalid
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
            raise forms.ValidationError(_("Je hebt een foutieve gebruikersnaam ingegeven."))
        return user

class AnswerForm(forms.Form):
    answer = forms.CharField(label=_("answer"), required=True)

class QuestionForm(forms.Form):
    question = forms.ModelChoiceField(queryset=RegistrationQuestion.objects.filter(in_use=True), empty_label=None, widget=forms.HiddenInput())
