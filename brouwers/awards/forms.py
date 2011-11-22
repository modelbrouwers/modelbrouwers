from django import forms
from models import Project, Category
from brouwers.general.models import UserProfile
import re

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('votes', 'nomination_date', 'nominator', 'rejected')
		widgets = {
			'url': forms.TextInput(attrs={'size':60}),
			'name': forms.TextInput(attrs={'size':60})
		}
	
	def clean_url(self):
		url = self.cleaned_data['url']
		match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
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
