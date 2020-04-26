import re

from django import forms
from django.utils.translation import ugettext as _

from brouwers.general.models import UserProfile

from .models import Category, Project, Vote


class ProjectForm(forms.ModelForm):
    url_pattern = 'modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)'

    class Meta:
        model = Project
        exclude = (
            'votes',
            'nomination_date',
            'rejected',
            'submitter',
            'last_reviewer'
        )
        widgets = {
            'url': forms.TextInput(attrs={'size': 60}),
            'name': forms.TextInput(attrs={'size': 60}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # do some processing if added from the board itself
        forum_id = self.initial.get('forum_id', None)
        topic_id = self.initial.get('topic_id', None)
        if forum_id and topic_id:
            url = 'https://modelbrouwers.nl/phpBB3/viewtopic.php?f={0}&t={1}'
            url = url.format(forum_id, topic_id)
            self.fields['url'].initial = url

            # check if this one exists
            if Project.objects.filter(url=url).exists():
                self.errors['url'] = [_("This project was already nominated.")]

        self.fields['url'].widget.attrs['placeholder'] = 'http://www.modelbrouwers.nl/phpBB3/viewtopic.php?f=42&t=10'

    def clean_url(self):
        url = self.cleaned_data['url']
        match = re.search(self.url_pattern, url)
        if not match:
            raise forms.ValidationError("Deze url wijst niet naar een forumtopic.")
        url = "http://www.%s" % match.group(0)
        return url

    def clean_brouwer(self):
        brouwer = self.cleaned_data['brouwer']
        try:
            profile = UserProfile.objects.get(forum_nickname__iexact=brouwer)
        except UserProfile.DoesNotExist:
            pass
        else:
            if profile.exclude_from_nomination:
                raise forms.ValidationError(_('This person does not wish to participate in the awards.'))
        return brouwer


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class YearForm(forms.Form):
    year = forms.IntegerField(required=False, label="Bekijk jaar")


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'category': forms.HiddenInput(attrs={'class': 'category'}),
            'project1': forms.HiddenInput(attrs={'class': 'project project1'}),
            'project2': forms.HiddenInput(attrs={'class': 'project project2'}),
            'project3': forms.HiddenInput(attrs={'class': 'project project3'}),
        }

    def __init__(self, *args, **kwargs):
        """ Improve performance by reducing the number of queries """
        queryset = kwargs.pop('queryset', None)
        super().__init__(*args, **kwargs)

        self.fields['project1'].error_messages['required'] = _("When voting,"
                                                               " you cannot leave the first place blank.")

        if queryset:
            choices = [(project.id, project) for project in queryset]
            choices.insert(0, (0, '-------'))

            self.fields['project1'].choices = choices

            if len(choices)-1 >= 2:
                self.fields['project2'].choices = choices
            else:
                self.fields['project2'].choices = choices[:1]

            if len(choices)-1 >= 3:
                self.fields['project3'].choices = choices
            else:
                self.fields['project3'].choices = choices[:1]

    def clean(self):
        cleaned_data = super().clean()
        project1 = cleaned_data.get('project1', None)
        project2 = cleaned_data.get('project2', None)
        project3 = cleaned_data.get('project3', None)
        if project1 and project3 and not project2:
            raise forms.ValidationError(_("The order of votes must be logical. "
                                          "Omitting the second place is not allowed."))
        return cleaned_data
