from datetime import date
import re

from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from models import *
from forms import ProjectForm, CategoryForm


from django.core.mail import send_mail

def index(request):
	return render_to_response('awards/base.html', {'user': request.user})

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
	return render_to_response('awards/category.html', RequestContext(request, {'form': form, 'allowed': allowed, 'status': status, 'categories': categories}))


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
	return render_to_response('awards/nomination.html', RequestContext(request, {'form': form, 'status': status, 'last_nominations': last_nominations})
	)

def nomination_valid(url, brouwer):
	match = re.search('modelbrouwers.nl/phpBB3/viewtopic.php\?f=(\d+)&t=(\d+)', url)
	if match:
		url = match.group(0)
		projects = Project.objects.filter(url__icontains = url)
		if projects:
			category = projects[0].category.name
			status = "<font color=\"Red\">Dit project is al genomineerd in de categorie \"%s\"</font>" % category
			return (False, status, False)
		else:
			profiles = UserProfile.objects.filter(forum_nickname__iexact = brouwer)
			if profiles:
				profile = profiles[0]
				if (profile.exclude_from_nomination==True):
					return (True, "<font color=\"Red\">De nominatie is in de database opgenomen, echter deze zal op verzoek van de brouwer niet in aanmerking komen voor een award.</font>", True)
				else:
					return (True, "De nominatie is toegevoegd", False)
			else:
				return (True, "De nominatie is toegevoegd", False)
	else:
		return (False, "<font color=\"Red\">De nominatie kon niet worden toegevoegd, de url wijst niet naar een forumtopic!</font>", False)

def category_list_nominations(request, id):
	category = Category.objects.get(id__exact = id)
	projects = category.project_set.all().order_by('pk')
	projects = projects.exclude(rejected=True)
	return render_to_response('awards/category_list_nominations.html', RequestContext(request, {'category': category, 'projects': projects}))
	

@user_passes_test(lambda u: u.is_authenticated(), login_url='/login/')
def vote(request):
	data = {}
	categories = Category.objects.all()
	year = date.today().year-1
	limit_date = date(year+1,1,15) #date where the voting ends
	if request.method=='POST':
		for cat in categories:
			try:
				project = get_object_or_404(Project, pk=request.POST[unicode(cat)])
				project.votes += 1
				project.save()
			except ValueError, KeyError:
				pass
		profile = request.user.get_profile()
		profile.last_vote = date.today()
		profile.save()
		voted = True;
		return render_to_response('awards/vote.html', RequestContext(request, {'voted': voted, 'year': year}))
	else:
		if date.today() <= limit_date:
			if (request.user.get_profile().last_vote.year == date.today().year):
				status = 'Je hebt al gestemd voor de editie van %s, bedankt!' % year
				voted = True;
				return render_to_response('awards/vote.html', RequestContext(request, {'status': status, 'voted': voted, 'year': year}))
			else:
				voted = False;
				for cat in categories:
					projects = Project.objects.filter(category__exact=cat)
					projects_valid = projects.filter(nomination_date__year = year)
					data[cat] = projects_valid.exclude(rejected=True)
				return render_to_response('awards/vote.html', RequestContext(request, {'data': data, 'voted': voted, 'year': year}))
		else:
			status = "De editie van %s is afgelopen, er kon gestemd worden tot en met %s. Vanaf %s tot %s kunt u stemmen voor de projecten uit %s." % (year, limit_date.strftime("%d-%m-%Y"), date(year+2,1,1).strftime("%d-%m-%Y"), date(limit_date.year+1, limit_date.month, limit_date.day).strftime("%d-%m-%Y"), year+1)
			return render_to_response('awards/vote.html', RequestContext(request, {'status': status, 'voted': True, 'year': year, 'year_now': year+1}))

def vote_overview(request):
	data = {}
	categories = Category.objects.all()
	year = date.today().year
	for cat in categories:
		projects = Project.objects.filter(category__exact=cat)
		projects_valid = projects.filter(nomination_date__year = year)
		data[cat] = projects_valid.exclude(rejected=True)
	return render_to_response('awards/vote_listing.html', RequestContext(request, {'data': data, 'year': year}))
