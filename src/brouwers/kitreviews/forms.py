from django import forms
from django.utils.translation import ugettext_lazy as _

from brouwers.albums.models import Album
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
    model_kit = forms.ModelChoiceField(queryset=ModelKit.objects.all(), required=False)

    class Meta:
        model = KitReview
        exclude = ('model_kit', 'html', 'reviewer')

    def __init__(self, user, *args, **kwargs):
        super(KitReviewForm, self).__init__(*args, **kwargs)
        # limit album selection to own albums
        # TODO: include group albums and public albums...
        self.fields['album'].queryset = Album.objects.filter(user=user, trash=False)
