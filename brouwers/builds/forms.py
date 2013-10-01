from django import forms
from django.core.exceptions import ObjectDoesNotExist
from models import Build

import re

class BrouwerSearchForm(forms.Form):
	nickname = forms.CharField(max_length=20)

class BuildForm(forms.ModelForm):
	class Meta:
		model = Build
		exclude = ('profile', 'nomination', 'user', 'slug', 'topic_id', 'forum_id', 'brand_name')
		widgets = {
			'url': forms.TextInput(attrs={'size':70}),
			'title': forms.TextInput(attrs={'size':70}),
			'img1': forms.TextInput(attrs={'size':70}),
			'img2': forms.TextInput(attrs={'size':70}),
			'img3': forms.TextInput(attrs={'size':70}),
			}
	
	def clean_url(self):
		url = self.cleaned_data['url']
		match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
		if not match:
			match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?t=(\d+)&f=(\d+)', url)
			if not match:
				raise forms.ValidationError("De url wijst niet naar een forumtopic.")
		self.cleaned_data['url'] = "http://www.%s" % match.group(0)
		return self.cleaned_data['url']
