from django import forms
from django.utils.translation import ugettext as _

from .models import *


class UploadForm(forms.Form):
    album = forms.ModelChoiceField(queryset=Album.objects.none(), empty_label=None)
    image_url = forms.URLField(label=_('image url'), required=False)

    def __init__(self, request, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        # TODO: add albums that are shared
        self.fields['album'].queryset = Album.objects.select_related(
            'cover'
        ).filter(
            user=request.user, trash=False
        ).order_by('-last_upload')


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = (
            'title',
            'description',
            'category',
            'public',
            'topic',
            'writable_to',
        )

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(public=True)


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ('auto_start_uploading', 'collapse_sidebar', 'hide_sidebar',
                  'sidebar_bg_color', 'sidebar_transparent', 'text_color',
                  'width')
