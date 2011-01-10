from django.shortcuts import get_object_or_404

from brouwers.general.shortcuts import render_to_response
from brouwers.awards.models import UserProfile
from forms import BrouwerSearchForm
from models import Build

def builders_overview(request):
	if request.method == "POST":
		form = BrouwerSearchForm(request.POST)
		if form.is_valid():
			brouwer = form.cleaned_data['nickname']
			profiles = UserProfile.objects.filter(forum_nickname__icontains = brouwer).order_by('forum_nickname')
			form = BrouwerSearchForm()
			return render_to_response(request, 'builds/profile_list.html', {'profiles': profiles, 'form': form})
	else:
		form = BrouwerSearchForm()
	return render_to_response(request, 'builds/base.html', {'form': form})
