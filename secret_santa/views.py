from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.translation import ugettext as _

from models import Couple, Participant, SecretSanta
from forms import EnrollForm
from utils import get_current_ss
from datetime import datetime

def index(request):
    secret_santa = get_current_ss(SecretSanta)
    initial = {'secret_santa': secret_santa, 'user': request.user}
    form = EnrollForm(initial=initial)
    participants = Participant.objects.filter(secret_santa=secret_santa).select_related('user').order_by('id')
    can_do_lottery = datetime.now() >= secret_santa.lottery_date
    return render(request, 'secret_santa/base.html', {
        'secret_santa': secret_santa,
        'form': form,
        'participants': participants,
        'can_do_lottery': can_do_lottery,
        'is_participant': secret_santa.is_participant(request.user),
        }
    )

# TODO: voorkeuren ingeven!
@login_required
def enroll(request):
    secret_santa = get_current_ss(SecretSanta)
    if request.method == "POST":
        if secret_santa.enrollment_open:
            initial = {'secret_santa': secret_santa, 'user': request.user}
            form = EnrollForm(request.POST, initial=initial)
            address_complete = request.user.profile.is_address_ok
            if form.is_valid() and  address_complete and not secret_santa.is_participant(request.user):
                participant = form.save(commit=False)
                participant.year = participant.secret_santa.year
                participant.save()
            elif not address_complete:
                messages.error(request, _("Your address details are incomplete."))
        else:
            messages.error(request, _("Signing up is not possible at this time."))
    return HttpResponseRedirect(reverse(index))

@user_passes_test(lambda u: u.is_authenticated() and u.is_staff, login_url='/login/')
def lottery(request):
    #clear old entries
    secret_santa = get_current_ss(SecretSanta)
    couples = []

    sending_participants = Participant.objects.filter(secret_santa=secret_santa).order_by('pk')
    receivers = list(sending_participants.order_by('?')) #randomize list of participants
    sending_participants2 = list(sending_participants)
    if sending_participants2[-1] == receivers[-1]:
        receivers[-1], receivers[-2] = receivers[-2], receivers[-1]

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
        messages.success(request, _("The lottery is done."))
    return HttpResponseRedirect(reverse(index))

@login_required
def receiver(request):
    secret_santa = get_current_ss(SecretSanta)
    receiver = None
    if datetime.now() >= secret_santa.lottery_date:
        if secret_santa.is_participant(request.user):
            try:
                # couple where user is the sender
                couple = Couple.objects.select_related('participant').get(
                    sender__user_id = request.user.id,
                    secret_santa = secret_santa
                    )
                return render(request, 'secret_santa/receiver.html', {'receiver': receiver, 'secret_santa': secret_santa })
            except Couple.DoesNotExist:
                messages.error(request, _("Your match does not exist."))
        else:
            messages.info(request, _("You're not a participant!"))
    else:
        messages.info(request, _("You can't view the lottery results yet."))
    return HttpResponseRedirect(reverse(index))
