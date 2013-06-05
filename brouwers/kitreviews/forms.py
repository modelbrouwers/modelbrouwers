from django import forms


from albums.models import Album
from models import *

class ModelKitForm(forms.ModelForm):
    class Meta:
        model = ModelKit
        exclude = ('duplicates', 'submitter')

class KitReviewForm(forms.ModelForm):
    class Meta:
        model = KitReview
        exclude = ('html', 'reviewer')

    def __init__(self, user, *args, **kwargs):
        super(KitReviewForm, self).__init__(*args, **kwargs)
        # limit album selection to own albums
        self.fields['album'].queryset = Album.objects.filter(user=user)
    