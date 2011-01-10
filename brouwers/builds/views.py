from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
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
	builds = Build.objects.all().order_by('-pk')[:15]
	return render_to_response(request, 'builds/base.html', {'form': form, 'builds': builds})

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
			return HttpResponseRedirect(reverse('build_detail', args=[build.id]))
	else:
		form = BuildForm()
	return render_to_response(request, 'builds/add.html', {'form': form})

@login_required
def edit(request, id):
	build = get_object_or_404(Build, pk=id)
	if request.method == "POST":
		form = BuildForm(request.POST, instance=build)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('build_detail', args=[id]))
	else:
		if build.profile != request.user.get_profile():
			return HttpResponseRedirect(reverse(builders_overview))
		form = BuildForm(instance=build)
	return render_to_response(request, 'builds/edit.html', {'form': form})
