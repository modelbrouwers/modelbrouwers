from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from brouwers.general.shortcuts import render_to_response
from brouwers.awards.models import UserProfile, Project
from forms import BrouwerSearchForm
from models import Build
from forms import BuildForm

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

@login_required
def add(request):
	if request.method == "POST":
		build = Build(profile = request.user.get_profile())
		form = BuildForm(request.POST, instance=build)
		if form.is_valid():
			build = form.save()
			try:
				nomination = Project.objects.get(url__icontains = form.cleaned_data['url'])
				build.nomination = nomination
				build.save()
			except ObjectDoesNotExist:
				pass
			return HttpResponseRedirect('/builds/%s' % build.id)
	else:
		form = BuildForm()
	return render_to_response(request, 'builds/add.html', {'form': form})
