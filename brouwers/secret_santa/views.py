from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test, login_required

from models import Couple, Participant, SecretSanta
from forms import EnrollForm
from utils import get_current_ss
from datetime import date, datetime

def index(request):
    secret_santa = get_current_ss(SecretSanta)
    initial = {'secret_santa': secret_santa, 'user': request.user}
    form = EnrollForm(initial=initial)
    participants = Participant.objects.filter(secret_santa=secret_santa).order_by('id')
    can_do_lottery = datetime.now() >= secret_santa.lottery_date
    return render(request, 'secret_santa/base.html', {
        'secret_santa': secret_santa, 
        'form': form, 
        'participants': participants,
        'can_do_lottery': can_do_lottery,
        'is_participant': secret_santa.is_participant(request.user),
        }
    )

@login_required
def enroll(request):
    secret_santa = get_current_ss(SecretSanta)
    if request.method == "POST":
        initial = {'secret_santa': secret_santa, 'user': request.user}
        form = EnrollForm(request.POST, initial=initial)
        if form.is_valid() and request.user.get_profile().is_address_ok and not secret_santa.is_participant(request.user):
            participant = form.save(commit=False)
            participant.year = participant.secret_santa.year
            participant.save()
    return HttpResponseRedirect(reverse(index))

@user_passes_test(lambda u: u.is_authenticated() and u.is_staff, login_url='/login/')
def lottery(request):
    #clear old entries
    secret_santa = get_current_ss(SecretSanta)
    couples = []
    
    sending_participants = Participant.objects.filter(secret_santa=secret_santa, verified=True).order_by('pk')
    receivers = list(sending_participants.order_by('?')) #randomize list of participants
    sending_participants2 = list(sending_participants)
    if sending_participants2[-1] == receivers[-1]:
        temp = receivers[-1]
        receivers[-1] = receivers[-2]
        receivers[-2] = temp
    
    already_sender = set()
    if sending_participants and not secret_santa.lottery_done:
        for receiver in receivers:
            senders = sending_participants.exclude(user=receiver.user) #exclude yourself - you don't send a present to yourself
            couple = Couple(receiver=receiver, secret_santa=secret_santa)
            for sender in senders: #dedicate a sender to the receiver
                if not sender in already_sender: #sender can't send twice
                    couple.sender = sender
                    already_sender.add(sender)
                    break    #break once a sender has been determined
            couple.save()
            couples.append(couple.id)
        
        secret_santa.lottery_done = True
        secret_santa.save()
        secret_santa.do_mailing()
    return HttpResponseRedirect('/secret_santa')

@login_required
def receiver(request):
    secret_santa = get_current_ss(SecretSanta)
    treshold = secret_santa.lottery_date
    senders = Participant.objects.filter(user=request.user, secret_santa=secret_santa).order_by('-year')
    receiver = None
    if senders and not (datetime.now() < treshold):
        couples = Couple.objects.filter(sender=senders[0]) #couple where user is the sender
        if couples:
            receiver = couples[0].receiver
        return render(request, 'secret_santa/receiver.html', {'receiver': receiver, 'secret_santa': secret_santa })
    else:
        return HttpResponseRedirect('/static/error.html') #FIXME: proper via messages oplossen
