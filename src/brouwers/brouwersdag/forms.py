from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import ShowCasedModel


class ShowCasedModelSignUpForm(forms.ModelForm):
    error_messages = {
        'limit_person': _('There is a limit of {limit} model(s) per person for this competition.'),
        'limit_participants': _('The maximum number of contestors is reached. You can no longer enter the competition'),
    }

    add_another = forms.BooleanField(label=_('Add another model'), required=False)

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

    def clean(self):
        """ Validate that the number of subscribed models isn't going over the limits """
        cleaned_data = super(ShowCasedModelSignUpForm, self).clean()

        # no limit cleaning required, model is not doing the competition
        if not cleaned_data.get('is_competitor'):
            return cleaned_data

        limit_per_person = self.competition.max_num_models
        limit_participants = self.competition.max_participants
        # if there are no limits, do no cleaning
        if not limit_participants and not limit_per_person:
            return cleaned_data

        base_models_qs = self.competition.showcasedmodel_set.filter(is_competitor=True)

        owner = cleaned_data.get('owner')
        if owner and limit_per_person:
            # check both owner and e-mail address
            num = base_models_qs.filter(owner=owner).count()
            if num >= limit_per_person:
                raise forms.ValidationError(self.error_messages['limit_person'].format(limit=limit_per_person))

        # always test the e-mail address
        email = cleaned_data.get('email')
        if email and limit_per_person:
            num = base_models_qs.filter(email=email).count()
            if num >= limit_per_person:
                raise forms.ValidationError(self.error_messages['limit_person'].format(limit=limit_per_person))

        # test that the absolute limit is not reached
        if limit_participants:
            num_participants = base_models_qs.values('email').distinct().count()
            if num_participants >= limit_participants:
                raise forms.ValidationError(self.error_messages['limit_participants'])

        return cleaned_data

    def save(self, *args, **kwargs):
        """ Set the competition when saving """
        if self.cleaned_data.get('is_competitor'):
            self.instance.competition = self.competition
        super(ShowCasedModelSignUpForm, self).save(*args, **kwargs)
