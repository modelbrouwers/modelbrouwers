from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from brouwers.general.decorators import login_required_403

from .models import *


@login_required_403
def set_online(request):
    # less awareness = better
    try:
        tracked_user = TrackedUser.objects.get(user=request.user)
        tracked_user.save()
    except TrackedUser.DoesNotExist:
        pass
    return HttpResponse(1)


#TODO: switch to permission required!
def get_online_users(request):
    if request.user.has_perms('online_users.add_trackeduser'):
        now = timezone.now()
        past = now - timedelta(minutes = MINUTES_FOR_ONLINE)
        users = TrackedUser.objects.filter(notificate=True, last_seen__gte=past)
        if users:
            return render(request, 'online_users/userlist.html', {'users': users})
    return HttpResponse(0)
