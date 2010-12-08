from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import user_passes_test, login_required

from brouwers.secret_santa.models import Participant, Couple

from datetime import date

def index(request):
	year = date.today().year
	participants = Participant.objects.all()
	participants = participants.filter(year = year).order_by('pk')
	return render_to_response('secret_santa/base.html', RequestContext(request, {'participants': participants, 'year': year}))

@user_passes_test(lambda u: u.is_authenticated() and u.is_staff, login_url='/login/')
def lottery(request):
	#clear old entries
	couples = Couple.objects.filter(sender__year__exact = date.today().year)
	if couples:
		for couple in couples:
			couple.delete()
	
	sending_participants = Participant.objects.all().filter(year__exact=date.today().year).order_by('pk')
	sending_participants = sending_participants.exclude(verified=False)
	receivers = sending_participants.order_by('?') #randomize list of participants
	
	already_sender = set()
	
	if sending_participants:
		for receiver in receivers:
			senders = sending_participants.exclude(user=receiver.user) #exclude yourself - you don't send a present to yourself
			couple = Couple()
			couple.receiver = receiver
			for sender in senders: #dedicate a sender to the receiver
				if not sender in already_sender: #sender can't send twice
					couple.sender = sender
					already_sender.add(sender)
					break	#break once a sender has been determined
			couple.save()
	return HttpResponseRedirect('/secret_santa')

@login_required
def receiver(request):
	treshold = date(2010,12,05)
	senders = Participant.objects.filter(user=request.user)
	receiver = None
	if senders and not (date.today() < treshold):
		couples = Couple.objects.filter(sender=senders[0]) #couple where user is the sender
		if couples:
			receiver = couples[0].receiver
		return render_to_response('secret_santa/receiver.html', RequestContext(request, {'receiver': receiver}))
	else:
		return HttpResponseRedirect('/media/error.html')
