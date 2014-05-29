from django import forms

from .models import ShowCasedModel


class ShowCasedModelSignUpForm(forms.ModelForm):
    class Meta:
        model = ShowCasedModel
        fields = (
            'owner',
            'owner_name',
            'email',
            'name',
            'brand',
            'scale',
            'remarks',
            'length',
            'width',
            'height',
            'topic',
            'is_competitor',
        )
        widgets = {
            'owner': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.competition = kwargs.pop('competition', None)
        super(ShowCasedModelSignUpForm, self).__init__(*args, **kwargs)
