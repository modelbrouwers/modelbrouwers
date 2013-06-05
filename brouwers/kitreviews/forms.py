from django import forms

from models import *

class ModelKitForm(forms.ModelForm):
    class Meta:
        model = ModelKit
        exclude = ('duplicates', 'submitter')

class KitReviewForm(forms.ModelForm):
    class Meta:
        model = KitReview
        exclude = ('html', 'reviewer')
    