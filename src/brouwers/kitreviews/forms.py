from django import forms
from django.utils.translation import ugettext_lazy as _

from brouwers.kits.models import Brand, ModelKit, Scale
from .models import KitReview


class ModelKitForm(forms.ModelForm):
    class Meta:
        model = ModelKit
        exclude = ('duplicates', 'submitter')


class FindModelKitForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label=_('Brand'), required=False)
    kit_number = forms.CharField(label=_('Kit number'), required=False)
    kit_name = forms.CharField(label=_('Kit name'), required=False)
    scale = forms.ModelChoiceField(queryset=Scale.objects.all(), label=_('Scale'), required=False)


class KitReviewForm(forms.ModelForm):
    model_kit = forms.ModelChoiceField(queryset=ModelKit.objects.all(), required=True)

    class Meta:
        model = KitReview
        fields = ['model_kit', 'raw_text', 'album', 'topic_id', 'external_topic_url', 'show_real_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(KitReviewForm, self).__init__(*args, **kwargs)
        # limit album selection to own albums
        # TODO: include group albums and public albums...
        self.fields['model_kit'].queryset = self.fields['model_kit'].queryset.select_related('brand')
        self.fields['album'].queryset = self.user.album_set.filter(trash=False)

    def save(self, *args, **kwargs):
        self.instance.reviewer = self.user
        return super(KitReviewForm, self).save(*args, **kwargs)
