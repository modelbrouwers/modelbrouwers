import re

from django import forms
from django.utils.translation import ugettext as _

from general.models import UserProfile
from .models import Project, Category, Vote


class ProjectForm(forms.ModelForm):
	url_pattern = 'modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)'

	class Meta:
		model = Project
		exclude = (
			'votes',
			'nomination_date',
			'nominator',
			'rejected',
			'submitter',
			'last_reviewer'
		)
		widgets = {
			'url': forms.TextInput(attrs={'size':60}),
			'name': forms.TextInput(attrs={'size':60}),
		}

	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args, **kwargs)
		# do some processing if added from the board itself
		forum_id = self.initial.get('forum_id', None)
		topic_id = self.initial.get('topic_id', None)
		if forum_id and topic_id:
			url = 'http://www.modelbrouwers.nl/phpBB3/viewtopic.php?f={0}&t={1}'
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

	def save(self, *args, **kwargs):
		instance = super(ProjectForm, self).save(*args, **kwargs)
		try:
			profile = UserProfile.objects.get(forum_nickname__iexact = instance.brouwer)
			if profile.exclude_from_nomination:
				#TODO: send message that nomination is entered but the builder wishes not to take part
				instance.rejected = True
				instance.save()
		except UserProfile.DoesNotExist:
			pass
		return instance

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category

class YearForm(forms.Form):
	year = forms.IntegerField(required=False, label="Bekijk jaar")

class VoteForm(forms.ModelForm):
	class Meta:
		model = Vote
		widgets = {
			'user': forms.HiddenInput(),
			'category': forms.HiddenInput(attrs={'class': 'category'}),
			'project1': forms.HiddenInput(attrs={'class': 'project1'}),
			'project2': forms.HiddenInput(attrs={'class': 'project2'}),
			'project3': forms.HiddenInput(attrs={'class': 'project3'}),
		}

	def __init__(self, *args, **kwargs):
		""" Improve performance by reducing the number of queries """
		queryset = kwargs.pop('queryset', None)
		super(VoteForm, self).__init__(*args, **kwargs)

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