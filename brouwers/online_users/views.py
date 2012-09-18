from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponse
from brouwers.general.shortcuts import render_to_response
from models import *
from datetime import datetime, timedelta

def set_online(request): 
    # login required, but just filter out the anonymous users.
    # less awareness = better
    if request.user.is_authenticated():
        try:
            tracked_user = TrackedUser.objects.get(user=request.user)
            tracked_user.save()
        except TrackedUser.ObjectDoesNotExist:
            pass
    return HttpResponse()

@permission_required('online_users.add_trackeduser')
def get_online_users(request):
    now = datetime.now()
    past = now - timedelta(minutes = MINUTES_FOR_ONLINE)
    users = TrackedUser.objects.filter(notificate=True, last_seen__gte=past)
    if users:
        return render_to_response(request, 'online_users/userlist.html', {'users': users})
    return HttpResponse(0)
