from django import forms
from django.utils.translation import gettext_lazy as _

from .models import GroupBuild, GroupbuildStatuses, Participant


class GroupBuildForm(forms.ModelForm):
    error_messages = {
        "start_pinned": _(
            "The start date cannot be edited if the build is outside of the concept state."
        ),
        "duration_pinned": _(
            "The duration cannot be edited if the build is outside of the concept state."
        ),
    }

    class Meta:
        model = GroupBuild
        fields = (
            "theme",
            "category",
            "description",
            "admins",
            "start",
            "duration",
            "rules",
            "rules_topic",
            "homepage_topic",
            "introduction_topic",
        )
        localized_fields = "__all__"

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.applicant_id:
            self.instance.applicant = request.user

    def save(self, *args, **kwargs):
        _created = self.instance.id is None and kwargs.get("commit", True)
        gb = super().save(*args, **kwargs)
        if _created and gb.applicant not in gb.admins.all():
            gb.admins.add(gb.applicant)
        return gb

    def clean_start(self):
        start = self.cleaned_data.get("start")
        if (
            self.instance.status != GroupbuildStatuses.concept
            and start != self.instance.start
        ):
            raise forms.ValidationError(self.error_messages["start_pinned"])
        return start

    def clean_duration(self):
        duration = self.cleaned_data.get("duration")
        if (
            self.instance.status != GroupbuildStatuses.concept
            and duration != self.instance.duration
        ):
            raise forms.ValidationError(self.error_messages["duration_pinned"])
        return duration


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ("model_name", "topic")


class SubmitForm(forms.ModelForm):
    class Meta:
        model = GroupBuild
        fields = ()  # no fields

    def save(self, *args, **kwargs):
        self.instance.status = GroupbuildStatuses.submitted
        return super().save(*args, **kwargs)
