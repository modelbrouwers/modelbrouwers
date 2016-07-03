from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

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

    def find_kits(self):
        results = ModelKit.objects.select_related('brand', 'scale')

        brand = self.cleaned_data['brand']
        if brand:
            results = results.filter(brand_id=brand.id)

        kit_number = self.cleaned_data['kit_number']
        if kit_number:
            results = results.filter(kit_number__icontains=kit_number)

        kit_name = self.cleaned_data['kit_name']
        if kit_name:
            name_parts = kit_name.split(' ')
            # order doesn't matter, just find the kits with names that have all
            # the search terms
            q_list = []
            for part in name_parts:
                q_list.append(Q(name__icontains=part))
            results = results.filter(*q_list)

        scale = self.cleaned_data['scale']
        if scale:
            results = results.filter(scale_id=scale.id)
        return results


class KitReviewForm(forms.ModelForm):
    model_kit = forms.ModelChoiceField(queryset=ModelKit.objects.all(), required=True)

    class Meta:
        model = KitReview
        fields = ['model_kit', 'raw_text', 'album', 'topic', 'external_topic_url', 'show_real_name']

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
