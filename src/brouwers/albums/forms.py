from django import forms
from django.utils.translation import gettext as _

from .models import Album, Category, Photo, Preferences


class AlbumQuerysetFormMixin(object):
    """
    Mixin that limits the albums for the Carousel slider to the
    logged in user.
    """

    def __init__(self, request=None, *args, **kwargs):
        assert request is not None
        super().__init__(*args, **kwargs)
        # TODO: add albums that are shared
        self.fields["album"].queryset = (
            Album.objects.select_related("cover")
            .filter(user=request.user, trash=False)
            .order_by("-last_upload")
        )


class UploadForm(AlbumQuerysetFormMixin, forms.Form):
    album = forms.ModelChoiceField(queryset=Album.objects.none(), empty_label=None)
    image_url = forms.URLField(label=_("image url"), required=False)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = (
            "title",
            "description",
            "category",
            "public",
            "topic",
            "writable_to",
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(public=True)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title:
            qs = self._meta.model.objects.filter(title=title, user=self.user)
            if qs.exists():
                msg = _("You already have an album with this title.")
                cleaned_data = self.add_error("title", forms.ValidationError(msg))
        return cleaned_data


class AlbumRestoreForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("trash",)
        widgets = {"trash": forms.HiddenInput}


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ("auto_start_uploading", "paginate_by_sidebar")


class PhotoForm(AlbumQuerysetFormMixin, forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("album", "description")


class PhotoRestoreForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("trash",)
        widgets = {"trash": forms.HiddenInput}
