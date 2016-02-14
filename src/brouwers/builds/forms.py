from __future__ import unicode_literals

from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db.models import Q

from brouwers.kits.models import ModelKit
from .models import Build, BuildPhoto


class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ('title', 'topic', 'topic_start_page', 'kits', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'date'}),
        }
        localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BuildForm, self).__init__(*args, **kwargs)
        self.fields['kits'].queryset = ModelKit.objects.select_related('brand', 'scale')


class BuildPhotoForm(forms.ModelForm):
    class Meta:
        model = BuildPhoto
        fields = ('photo', 'photo_url', 'order')
        widgets = {
            'photo': forms.HiddenInput,
            'order': forms.HiddenInput,
        }


class BuildSearchForm(forms.Form):
    q = forms.CharField()

    def get_search_results(self):
        assert self.is_valid()

        q = self.cleaned_data['q']
        results = []

        # find users first
        user = get_user_model().objects.filter(username__iexact=q).first()

        if user:
            results.append({
                'display': user.username,
                'url': reverse('builds:user_build_list', kwargs={'user_id': user.id})
            })

        builds = Build.objects.select_related('user').filter(
            Q(user__username__icontains=q) | Q(title__icontains=q)
        ).order_by('title')
        for build in builds:
            results.append({
                'display': '{0.user.username} - {0.title}'.format(build),
                'url': build.get_absolute_url(),
            })
        return results


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
