from django.core.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from brouwers.awards.forms import ProfileForm, UserForm
from brouwers.awards.models import UserProfile

def index(request):
	return render_to_response('base.html', {'user': request.user})

@user_passes_test(lambda u: u.is_authenticated(), login_url='/awards/login/')
def profile(request):
	forms = {}
	if request.method=='POST':
		forms['profileform'] = ProfileForm(request.POST, instance=request.user.get_profile())
		forms['userform'] = UserForm(request.POST, instance=request.user)
		
		if forms['profileform'].is_valid():
			forms['profileform'].save()
			if forms['profileform'].cleaned_data['exclude_from_nomination']:
				projects = Project.objects.filter(brouwer__iexact=request.user.get_profile().forum_nickname)
				for project in projects:
					project.rejected = True
					project.save()

		if forms['userform'].is_valid():
			forms['userform'].save()
		return render_to_response('general/profile.html', RequestContext(request, forms))
	else:
		forms['profileform'] = ProfileForm(instance=request.user.get_profile())
		forms['userform'] = UserForm(instance=request.user)
		return render_to_response('general/profile.html', RequestContext(request, forms))
