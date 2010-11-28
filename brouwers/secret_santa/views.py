from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from brouwers.secret_santa.models import Participant

from datetime import date

def index(request):
	year = date.today().year
	participants = Participant.objects.all()
	participants = participants.filter(year = year)
	return render_to_response('secret_santa/base.html', RequestContext(request, {'participants': participants, 'year': year}))
#	return HttpResponseRedirect('/profile/')
