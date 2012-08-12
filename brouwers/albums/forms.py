from django import forms
from django.db.models import Q
from django.utils.translation import ugettext as _
from models import *

import re
from datetime import datetime

def cln_build_report(form):
    url = form.cleaned_data['build_report']
    if not url:
        return url
    match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
    if not match:
        raise forms.ValidationError(_("This link doesn't point to a valid forum topic. Please correct the error"))
    url = "http://www.%s" % match.group(0)
    return url

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('user', 'created', 'modified', 'last_upload', 'views', 'votes', 'order', 'trash', 'cover')
        
    def clean_build_report(self):
        return cln_build_report(self)

class EditAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'description', 'build_report', 'category', 'cover', 'order', 'public', 'writable_to', 'trash')
        widgets = {
            'description': forms.Textarea(),
        }
    
    def __init__(self, *args, **kwargs):
        super(EditAlbumForm, self).__init__(*args, **kwargs)
        album = kwargs.pop('instance')
        self.fields['cover'].queryset = Photo.objects.filter(album=album)
    
    def save(self, *args, **kwargs):
        if self.instance.trash:
            self.instance.title = "trash_%s_%s" % (datetime.now().strftime('%d%m%Y_%H.%M.%s'), self.instance.title)
        super(EditAlbumForm, self).save(*args, **kwargs)
    
    def clean_build_report(self):
        return cln_build_report(self)

class AmountForm(forms.Form):
    amount = forms.IntegerField(required=False, min_value=1, max_value=50)

class PickAlbumForm(forms.Form):
    album = forms.ModelChoiceField(queryset=Album.objects.none(), empty_label=None)
    
    def __init__(self, user, *args, **kwargs):
        try:
            browse = kwargs.pop('browse')
        except KeyError: #key not suplied
            browse = False
        super(PickAlbumForm, self).__init__(*args, **kwargs)
        own_albums = Album.objects.filter(user=user, writable_to="u", trash=False)
        public_albums = Album.objects.filter(writable_to="o", trash=False)
        self.fields['album'].queryset = (own_albums | public_albums).order_by('-writable_to')
        if browse:
            self.fields['album'].required = False

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('id', 'description', 'order')
        widgets = {
            'description': forms.Textarea(),
        }

class EditPhotoForm(forms.ModelForm):
    set_as_cover_photo = forms.BooleanField(required=False)
    class Meta:
        model = Photo
        fields = ('album', 'description', 'order', 'set_as_cover_photo')
        widgets = {
            'description': forms.Textarea(),
        }
    
    def __init__(self, *args, **kwargs):
        super(EditPhotoForm, self).__init__(*args, **kwargs)
        photo = kwargs['instance']
        albums = Album.objects.filter(Q(user=photo.user)|Q(public=True), trash=False)
        self.fields['album'].queryset = albums
        self.fields['album'].empty_label = None
    
    def save(self, *args, **kwargs):
        super(EditPhotoForm, self).save(*args, **kwargs)
        if self.fields['set_as_cover_photo']:
            self.instance.album.cover = self.instance
            self.instance.album.save()

class AddPhotoForm(forms.ModelForm):
    class Meta:
        fields = ('album', 'image')

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        widgets = {
            'user': forms.HiddenInput(),
        }

class SearchForm(forms.Form):
    search = forms.CharField(max_length=256, label=_("Keywords"))

