from django import forms

from brouwers.awards.models import Project
from brouwers.general.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'street', 'number', 'postal', 'city', 'province', 'country', # address
            'exclude_from_nomination', # awards
            'allow_sharing', # privacy
        )

    def save(self, *args, **kwargs):
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        if profile.exclude_from_nomination:
            # TODO
            projects = Project.objects.filter(brouwer__iexact=profile.forum_nickname)
            projects.update(rejected=True)
