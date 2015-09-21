from django import forms

from brouwers.kits.models import ModelKit
from brouwers.kits.widgets import ModelKitSelect
from .models import Build, BuildPhoto


class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ('title', 'topic', 'topic_start_page', 'kits', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'date'}),
            'kits': ModelKitSelect
        }
        localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BuildForm, self).__init__(*args, **kwargs)
        self.fields['kits'].queryset = ModelKit.objects.select_related('brand', 'scale')


class BuildPhotoForm(forms.ModelForm):
    class Meta:
        model = BuildPhoto
        fields = ('build', 'photo', 'photo_url', 'order')
        widgets = {
            'photo': forms.TextInput,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        photos = kwargs.pop('photos')
        super(BuildPhotoForm, self).__init__(*args, **kwargs)

        self.fields['photo'].choices = photos
        self.fields['build'].queryset = self.fields['build'].queryset.filter(user=user)


class BaseBuildPhotoInlineFormSet(forms.BaseInlineFormSet):

    def _get_possible_buildphotos(self, form):
        if not hasattr(self, '_possible_buildphotos'):
            qs = form.fields['id'].queryset.values_list('pk', flat=True)
            self._possible_buildphotos = [(pk, pk) for pk in qs]
        return self._possible_buildphotos

    def add_fields(self, form, index):
        super(BaseBuildPhotoInlineFormSet, self).add_fields(form, index)
        # performance optimization
        form.fields['id'].choices = self._get_possible_buildphotos(form)


# class BuildFormForum(forms.ModelForm):

#     """
#     Form to enable quick instantiating of a Build object trough GET QueryDict
#     """

#     class Meta:
#         model = Build
#         fields = ('topic', 'title')

#     def __init__(self, request, *args, **kwargs):
#         self.request = request
#         super(BuildFormForum, self).__init__(*args, **kwargs)

#     def get_build(self):
#         """
#         Pre-fill some build attributes based on GET parameters
#         """
#         build = Build(
#             topic_id=self.cleaned_data['topic_id'],
#             user_id=self.request.user.id,
#             title=self.cleaned_data['title'],
#         )

#         # Try to parse the scale
#         pattern = re.compile(r'1[:/](\d{1,4})')
#         match = re.search(pattern, build.title)
#         if match:
#             build.scale, created = Scale.objects.get_or_create(scale=match.group(1))

#         # see if we can match a brand...
#         bits = build.title.split()
#         for bit in bits:
#             build.brand = Brand.objects.filter(name__iexact=bit).first()

#         return build
