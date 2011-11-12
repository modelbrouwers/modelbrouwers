from django import forms

from models import Project, Category

from django.utils.translation import ugettext_lazy as _

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('votes', 'nomination_date', 'nominator')
		widgets = {
			'url': forms.TextInput(attrs={'size':60}),
			'name': forms.TextInput(attrs={'size':60})
		}

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
