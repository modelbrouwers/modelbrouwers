from django.forms import ModelForm, TextInput
from models import Project, Category

class ProjectForm(ModelForm):
	class Meta:
		model = Project
		exclude = ('votes', 'nomination_date', 'nominator')
		widgets = {
			'url': TextInput(attrs={'size':'60'}),
			'name': TextInput(attrs={'size':'60'})
		}

class CategoryForm(ModelForm):
	class Meta:
		model = Category
