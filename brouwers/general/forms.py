from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from models import UserProfile

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
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2
    
    def clean_forum_nickname(self):
        nickname = self.cleaned_data['forum_nickname']
        try:
            UserProfile.objects.get(forum_nickname=nickname)
            raise forms.ValidationError(_("Deze forumnickname is al in gebruik bij een andere user op deze website."))
            return nickname
        except UserProfile.DoesNotExist:
            return nickname
    
    def save(self, commit=True):
        forum_nickname = self.cleaned_data['forum_nickname']
        username = forum_nickname.replace(" ", "_") #TODO: lower() might be needed
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
        username = username.replace(" ", "_") #TODO: lower() might be needed
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
