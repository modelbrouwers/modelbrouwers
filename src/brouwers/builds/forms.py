from __future__ import unicode_literals

from django import forms
from django.urls import reverse, reverse_lazy
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
    q = forms.CharField(widget=forms.TextInput(
        attrs={'data-url': reverse_lazy('api:builds:search')}
    ))

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
