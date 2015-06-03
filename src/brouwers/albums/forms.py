from django import forms
from django.conf import settings
from django.db.models import Q
from django.utils.translation import ugettext as _

from .models import *
from .utils import admin_mode

import urllib2


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


class CreateAlbumForm(forms.ModelForm):
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
        super(CreateAlbumForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(public=True)


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ('auto_start_uploading', 'collapse_sidebar', 'hide_sidebar',
                  'sidebar_bg_color', 'sidebar_transparent', 'text_color',
                  'width')







def albums_as_choices(querysets, trash=False):
    albums = []
    for qs_dict in querysets:
        temp = []
        for album in qs_dict['qs']:
            label = album.__unicode__()
            temp.append([album.id, label])
        if temp:
            albums.append([qs_dict['optgroup'], temp])
    return albums


class PickAlbumForm(forms.Form):
    album = forms.ModelChoiceField(queryset=Album.objects.none(), empty_label=None)

    def __init__(self, user, *args, **kwargs):
        browse = kwargs.pop('browse', False)
        trash = kwargs.pop('trash', False)
        admin = kwargs.pop('admin_mode', admin_mode(user))
        super(PickAlbumForm, self).__init__(*args, **kwargs)
        # own_albums = Album.objects.filter(user=user, writable_to="u", trash=False).order_by('order', 'title')

        if admin:
            q = Q(trash=trash)
        else:
            q = Q(user=user, trash=trash)

        own_albums = Album.objects.filter(q).order_by('order', 'title')
        group_albums = Album.objects.filter(
            writable_to = "g",
            trash = trash,
            albumgroup__in = user.albumgroup_set.all()
            ).order_by('order', 'title')
        public_albums = Album.objects.filter(writable_to="o", trash=trash).order_by('order', 'title')

        #order is important here
        querysets = [
            {'optgroup': _("Own albums"), 'qs': own_albums},
            {'optgroup': _("Group albums"), 'qs': group_albums},
            {'optgroup': _("Public albums"), 'qs': public_albums},
            ]

        self.fields['album'].queryset = (own_albums | public_albums | group_albums).select_related('user')
        self.fields['album'].choices = albums_as_choices(querysets, trash=trash)
        if browse:
            self.fields['album'].required = False


class PickOwnAlbumForm(PickAlbumForm):
    def __init__(self, user, *args, **kwargs):
        super(PickOwnAlbumForm, self).__init__(user)

        own_albums = Album.objects.select_related('user').filter(user=user, trash=False).order_by('order', 'title')
        group_albums = Album.objects.filter(
            writable_to = "g",
            trash = False,
            albumgroup__in = user.albumgroup_set.all()
            ).order_by('order', 'title')

        querysets = [
            {'optgroup': _("Own albums"), 'qs': own_albums},
            {'optgroup': _("Group albums"), 'qs': group_albums},
            ]
        self.fields['album'].queryset = (own_albums | group_albums).select_related('user')
        self.fields['album'].choices = albums_as_choices(querysets, trash=False)


class OrderAlbumForm(PickAlbumForm):
    album_before = forms.ModelChoiceField(queryset=Album.objects.none(), required=False)
    album_after = forms.ModelChoiceField(queryset=Album.objects.none(), required=False)

    def __init__(self, user, *args, **kwargs):
        super(OrderAlbumForm, self).__init__(user, *args, **kwargs)
        self.fields['album_before'].queryset = self.fields['album'].queryset
        self.fields['album_after'].queryset = self.fields['album'].queryset


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

    def __init__(self, user, *args, **kwargs):
        super(EditPhotoForm, self).__init__(*args, **kwargs)
        photo = kwargs['instance']

        if admin_mode(user):
            albums = Album.objects.all()
        else:
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

class UploadFromURLForm(forms.Form):
    url = forms.URLField(required=False, label=_("link"), help_text=_("Upload a picture from url"))

    def clean_url(self):
        url = self.cleaned_data['url']
        if url != '':
            try:
                d = urllib2.urlopen(url)
                content_type = d.info()['Content-Type']
                valid = False
                for ext in settings.VALID_IMG_EXTENSIONS:
                    valid_content_type = "image/%s" % ext.replace('.', '')
                    if valid_content_type in content_type:
                        valid = True
                        break;
                if not valid:
                    raise forms.ValidationError(_("Make sure the link points to a jpg or png image."))
            except urllib2.HTTPError:
                raise forms.ValidationError(_("Could not download the image from the url"))
        return url


class SearchForm(forms.Form):
    search = forms.CharField(max_length=256, label=_("Keywords"))

