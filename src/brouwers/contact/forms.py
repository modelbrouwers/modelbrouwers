from django import forms

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3(action="contact"))

    class Meta:
        model = ContactMessage
        fields = ("name", "email", "message")
