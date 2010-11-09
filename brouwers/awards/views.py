from datetime import date
import re

from django.db.models import Q
from django.db.models.query import QuerySet
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test

from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404

from models import *
from forms import ProjectForm, CategoryForm

def index(request):
	return render_to_response('awards/base.html', {'user': request.user})

def get_or_create_profile(user):
	try:
		profile = user.get_profile()
	except ObjectDoesNotExist:
		profile = UserProfile()
		profile.user = user
		profile.save()
	return profile

def register(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)
		if form.is_valid(): #dinges toevoegen voor als 't fout is
			form.save()
			new_user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
			login(request, new_user)
			return HttpResponseRedirect('/awards/')
		else:
			return render_to_response('awards/register.html', RequestContext(request, {'form': form}))
	else:
		form = UserCreationForm()
		return render_to_response('awards/register.html', RequestContext(request, {'form': form}))

def custom_login(request):    
    next_page = request.REQUEST.get('next')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure next_page isn't garbage.
            if not next_page or ' ' in next_page:
                next_page = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(next_page)
    else:
        form = AuthenticationForm(request)
    return render_to_response('awards/login.html', RequestContext(request, {
        'form': form,
        'next': next_page,
    }))

def custom_logout(request):
	next_page = request.GET.get('next')
	if not next_page or ' ' in next_page:
		next_page = "/awards/?logout=1"
	logout(request)
	return HttpResponseRedirect(next_page)


def category(request):
	status = ''
	allowed = False
	categories = Category.objects.all()
	if request.user.groups.filter(name__iexact="moderators"):
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
	last_nominations = Project.objects.filter(Q(nomination_date__year=date.today().year-1) | Q(nomination_date__year = date.today().year)).order_by('-pk')[:15]
	if request.method == 'POST':
		form = ProjectForm(request.POST)
		if form.is_valid(): #check op url
			url = request.POST['url']
			if url_valid(url):
				new_nomination = form.save()
				form = ProjectForm()
				status = "Nominatie is toegevoegd"
			else:
				status = "<font color=\"Red\">De nominatie kon niet worden toegevoegd, de url wijst niet naar een forumtopic!</font>"
	else:
		form = ProjectForm()
	return render_to_response('awards/nomination.html', RequestContext(request, {'form': form, 'status': status, 'last_nominations': last_nominations})
	)

def url_valid(url):
	url_re = re.compile('http://www.modelbrouwers.nl/phpBB3/viewtopic.php\?f=\d+&t=\d+')
	match = url_re.match(url)
	
	url_re2 = re.compile('modelbrouwers.nl/phpBB3/viewtopic.php\?f=\d+&t=\d+')
	match2 = url_re2.search(url)
	if match or match2:
		return True
	else:
		return False

def category_list_nominations(request, id):
	category = Category.objects.get(id__exact = id)
	projects = category.project_set.all().order_by('pk')
	return render_to_response('awards/category_list_nominations.html', RequestContext(request, {'category': category, 'projects': projects}))
	

@user_passes_test(lambda u: u.is_authenticated(), login_url='/awards/login/')
def vote(request):
	data = {}
	categories = Category.objects.all()
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
		return render_to_response('awards/vote.html', RequestContext(request, {'voted': voted}))
	else:
		if (get_or_create_profile(request.user).last_vote.year == date.today().year):
			status = 'Je hebt dit jaar al gestemd, bedankt!'
			voted = True;
			return render_to_response('awards/vote.html', RequestContext(request, {'status': status, 'voted': voted}))
		else:
			voted = False;
			for cat in categories:
				data[cat] = Project.objects.filter(category__exact=cat)
			return render_to_response('awards/vote.html', RequestContext(request, {'data': data, 'voted': voted}))
