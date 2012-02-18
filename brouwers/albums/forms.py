from django import forms
from django.utils.translation import ugettext as _
from models import *

import re
#from datetime import date

class AlbumForm(forms.ModelForm):
	class Meta:
		model = Album
		exclude = ('user', 'created', 'modified', 'views', 'votes', 'order', 'trash')
		
	
	def clean_build_report(self):
		url = self.cleaned_data['build_report']
		if not url:
			return url
		match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
		if not match:
			raise forms.ValidationError(_("This link doesn't point to a valid forum topic. Please correct the error"))
		url = "http://www.%s" % match.group(0)
		return url

class AmountForm(forms.Form):
	amount = forms.IntegerField(required=False, min_value=1, max_value=50)

class PickAlbumForm(forms.Form):
	album = forms.ModelChoiceField(queryset=Album.objects.none(), empty_label=None)
	
	def __init__(self, user, *args, **kwargs):
		super(PickAlbumForm, self).__init__(*args, **kwargs)
		own_albums = Album.objects.filter(user=user, writable_to="u", trash=False)
		public_albums = Album.objects.filter(writable_to="o", trash=False)
		self.fields['album'].queryset = (own_albums | public_albums).order_by('-writable_to')

class PhotoForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ('id', 'description', 'order')
		widgets = {
			'description': forms.Textarea(),
		}
