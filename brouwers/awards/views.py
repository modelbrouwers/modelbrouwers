from datetime import date
import re

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test, login_required

from django.http import HttpResponseRedirect
from django.template import RequestContext
from brouwers.general.shortcuts import render_to_response
from django.shortcuts import get_object_or_404

from models import *
from forms import ProjectForm, CategoryForm
from brouwers.general.models import UserProfile

#TODO: link the user submitted in a nomination to an existing profile on the site
def find_profile(brouwer):
	try:
		profile = UserProfile.objects.get(forum_nickname__iexact=brouwer)
		return profile
	except ObjectDoesNotExist:
		return False

def category(request):
	status = ''
	allowed = False
	categories = Category.objects.all()
	if (request.user.groups.filter(name__iexact="moderators") or request.user.is_superuser):
		allowed = True
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			new_category = form.save()
			form = CategoryForm()
			status = "Nieuwe categorie is toegevoegd"
	else:
		form = CategoryForm()
	return render_to_response(request, 'awards/category.html', {'form': form, 'allowed': allowed, 'status': status, 'categories': categories})


def nomination(request):
	status = ''
	last_nominations = Project.objects.filter(Q(nomination_date__year=date.today().year-1) | Q(nomination_date__year = date.today().year)).order_by('-pk')
	last_nominations = last_nominations.exclude(rejected=True)[:15]
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			url = form.cleaned_data['url']
			brouwer = form.cleaned_data['brouwer']
			valid, status, exclude = nomination_valid(url, brouwer)
			if valid:
					new_nomination = form.save()
					if exclude:
						new_nomination.rejected = True
						new_nomination.save()
					if request.user.is_authenticated():
						new_nomination.nominator = request.user.get_profile()
						new_nomination.save()
					form = ProjectForm()
	else:
		form = ProjectForm()
	return render_to_response(request, 'awards/nomination.html', {'form': form, 'status': status, 'last_nominations': last_nominations})

def nomination_valid(url, brouwer):
	match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
	valid = True
	status = "De nominatie is toegevoegd"
	exclude = False
	if match:
		url = match.group(0)
		projects = Project.objects.filter(url__icontains = url)
		if projects:
			category = projects[0].category.name
			valid, status = False, "<font color=\"Red\">Dit project is al genomineerd in de categorie \"%s\"</font>" % category
		profiles = UserProfile.objects.filter(forum_nickname__iexact = brouwer)
		if profiles:
			profile = profiles[0]
			if (profile.exclude_from_nomination==True):
				status = "<font color=\"Red\">De nominatie is in de database opgenomen, echter deze zal op verzoek van de brouwer niet in aanmerking komen voor een award.</font>"
				exclude = True
	else:
		valid, status= False, "<font color=\"Red\">De nominatie kon niet worden toegevoegd, de url wijst niet naar een forumtopic!</font>"
	return(valid, status, exclude)

def category_list_nominations(request, id):
	category = Category.objects.get(id__exact = id)
	projects = category.project_set.all().filter(nomination_date__year = date.today().year)
	projects = projects.exclude(rejected=True)
	return render_to_response(request, 'awards/category_list_nominations.html', {'category': category, 'projects': projects})
	
@login_required
def vote(request):
	data = {}
	categories = Category.objects.all()
	year = date.today().year-1
	limit_date = date(year+1,1,15) #date where the voting ends
	profile = request.user.get_profile()
	if request.method=='POST':
		for cat in categories:
			try:
				project = get_object_or_404(Project, pk=request.POST[unicode(cat)])
				project.votes += 1
				project.save()
				profile.categories_voted.add(cat)
				profile.save()
			except (ValueError, KeyError):
				pass
		profile.last_vote = date.today()
		profile.save()
		voted = True;
		return HttpResponseRedirect('/awards/vote/scores/')
#		return render_to_response(request, 'awards/vote.html', {'voted': voted, 'year': year})
	else:
		if date.today() <= limit_date:
			if profile.last_vote.year < date.today().year:
				profile.categories_voted.clear()
			if (profile.last_vote.year == date.today().year) and (categories.count() == profile.categories_voted.count()):
#				status = 'Je hebt al gestemd voor de editie van %s, bedankt!' % year
#				voted = True;
#				return render_to_response(request, 'awards/vote.html', {'status': status, 'voted': voted, 'year': year})
				return HttpResponseRedirect('/awards/vote/scores/')
			else:
				categories_voted = profile.categories_voted.all()
				categories = categories.exclude(id__in=categories_voted)
				voted = False;
				for cat in categories:
					projects = Project.objects.filter(category__exact=cat)
					projects_valid = projects.filter(nomination_date__year = year).exclude(rejected=True)
					if not projects_valid:
						profile.categories_voted.add(cat)
						profile.save()
					data[cat] = projects_valid
				return render_to_response(request, 'awards/vote.html', {'data': data, 'voted': voted, 'year': year})
		else:
			status = "De editie van %s is afgelopen, er kon gestemd worden tot en met %s. Vanaf %s tot %s kunt u stemmen voor de projecten uit %s." % (year, limit_date.strftime("%d-%m-%Y"), date(year+2,1,1).strftime("%d-%m-%Y"), date(limit_date.year+1, limit_date.month, limit_date.day).strftime("%d-%m-%Y"), year+1)
			return render_to_response(request, 'awards/vote.html', {'status': status, 'voted': True, 'year': year})

def vote_overview(request):
	data = {}
	categories = Category.objects.all()
	year = date.today().year
	for cat in categories:
		projects = Project.objects.filter(category__exact=cat)
		projects_valid = projects.filter(nomination_date__year = year)
		data[cat] = projects_valid.exclude(rejected=True)
	return render_to_response(request, 'awards/vote_listing.html', {'data': data, 'year': year})

@user_passes_test(lambda u: u.is_authenticated(), login_url='/login/')
def scores(request):
	year = date.today().year
	if request.user.get_profile().last_vote.year != year:
		return HttpResponseRedirect('/awards/vote/')
	data = []
	voters = UserProfile.objects.filter(last_vote__year = year).count()
	year = date.today().year-1
	categories = Category.objects.all()
	categories_voted = request.user.get_profile().categories_voted.all()
	categories = categories.filter(id__in=categories_voted)
	for category in categories:
		projects = Project.objects.filter(category__exact=category).exclude(rejected=True).order_by('-votes')
		votes_total = 0
		if projects:
			for project in projects:
				votes_total += project.votes
			data.append({'category': category, 'projects': projects[:5], 'total': votes_total})
	return render_to_response(request, 'awards/vote_scores.html', {'data': data, 'year': year, 'voters': voters})
