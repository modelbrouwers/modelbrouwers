from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponse
from django.shortcuts import render
from models import *
from datetime import datetime, timedelta

def set_online(request): 
    # login required, but just filter out the anonymous users.
    # less awareness = better
    if request.user.is_authenticated():
        try:
            tracked_user = TrackedUser.objects.get(user=request.user)
            tracked_user.save()
        except TrackedUser.DoesNotExist:
            pass
    return HttpResponse()


def get_online_users(request):
    if request.user.has_perms('online_users.add_trackeduser'):
        now = datetime.now()
        past = now - timedelta(minutes = MINUTES_FOR_ONLINE)
        users = TrackedUser.objects.filter(notificate=True, last_seen__gte=past)
        if users:
            return render(request, 'online_users/userlist.html', {'users': users})
    return HttpResponse(0)
