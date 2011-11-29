from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from brouwers.general.models import UserProfile
from brouwers.general.shortcuts import render_to_response, voting_enabled
from models import *
from forms import ProjectForm, CategoryForm, YearForm
from datetime import date
import re

#TODO: link the user submitted in a nomination to an existing profile on the site
def find_profile(brouwer):
	try:
		profile = UserProfile.objects.get(forum_nickname__iexact=brouwer)
		return profile
	except ObjectDoesNotExist:
		return False

def category(request):
	categories = Category.objects.all()
	return render_to_response(request, 'awards/category.html', {'categories': categories})

def nomination(request):
	year = date.today().year
	last_nominations = Project.objects.filter(Q(nomination_date__year=date.today().year-1) | Q(nomination_date__year = date.today().year), rejected=False).order_by('-pk')[:15]
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid():
			new_nomination = form.save()
			if new_nomination.rejected:
				messages.info(request, "De nominatie zal niet stembaar zijn op verzoek van de brouwer zelf.")
			else:
				messages.success(request, "De nominatie is toegevoegd.")
			if request.user.is_authenticated():
				new_nomination.nominator = request.user.get_profile()
				new_nomination.save()
			return HttpResponseRedirect(reverse(nomination))
	else:
		form = ProjectForm()
	return render_to_response(request, 'awards/nomination.html', {'form': form, 'last_nominations': last_nominations, 'current_year': year})

def category_list_nominations(request, id_):
	category = get_object_or_404(Category, pk = id_)
	projects = category.project_set.all().filter(nomination_date__year = date.today().year)
	projects = projects.exclude(rejected=True)
	return render_to_response(request, 'awards/category_list_nominations.html', {'category': category, 'projects': projects})
	
@login_required
def vote(request):
	data = {}
	categories = Category.objects.all()
	year = date.today().year-1
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
		return HttpResponseRedirect('/awards/vote/scores/')
	else:
		if voting_enabled():
			if profile.last_vote.year < date.today().year:
				profile.categories_voted.clear()
			if (profile.last_vote.year == date.today().year) and (categories.count() == profile.categories_voted.count()):
				return HttpResponseRedirect('/awards/vote/scores/')
			else:
				categories_voted = profile.categories_voted.all()
				categories = categories.exclude(id__in=categories_voted)
				voted = False;
				for cat in categories:
					projects = Project.objects.filter(category__exact=cat)
					projects_valid = projects.filter(nomination_date__year = year).exclude(rejected=True)
					if not projects_valid.exists():
						profile.categories_voted.add(cat)
						profile.save()
					data[cat] = projects_valid
				return render_to_response(request, 'awards/vote.html', {'data': data, 'voted': voted, 'year': year})
		else:
			status = "De editie van %s is afgelopen, er kan niet meer gestemd worden" % year
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

def winners(request):
	form = YearForm(request.GET)
	today = date.today()
	last_year = today.year-1
	if form.is_valid():
		year = form.cleaned_data['year']
	if not year or not form.is_valid():
		year = last_year
	#year redirects
	if year >= today.year:
		if voting_enabled() and year == today.year:
			messages.info(request, "Het stemmen loopt nog, u kan nog geen winnaars voor dit jaar bekijken. U bent omgeleid naar de tussenstand.")
			return HttpResponseRedirect(reverse(scores))
		year = today.year-1
		messages.info(request, "Ook wij kunnen helaas niet in de toekomst kijken... u ziet dus de resultaten van editie %s." % year)
		return HttpResponseRedirect("%s?year=%s" % (reverse(winners), year))
		#actual data fetching
	data = []
	categories = Category.objects.all()
	for category in categories:
		projects = Project.objects.filter(category=category, nomination_date__year=year).order_by('-votes')
		if projects.exists():
			top_three = list(projects[:3])
			#ordering: first in the middle, second left, third right
			try:
				top_three[1], top_three[0] = top_three[0], top_three[1]
			except IndexError:
				#there's only one element (since the second is an index out of range)
				#do nothing
				top_three = [None, top_three[0], None]
			data.append({'category': category, 'top_three': top_three})
	return render_to_response(request, 'awards/winners.html', {'year': year, 'data': data, 'form': form})
