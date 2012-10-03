from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json

from models import UserProfile

@login_required
def search_users(request):
    inputresults = request.GET.__getitem__('term').split(' ')
    query = []
    for value in inputresults:
        q = Q(forum_nickname__icontains=value) | \
            Q(user__first_name__icontains=value) | \
            Q(user__last_name__icontains=value)
        query.append(q)
    if len(query) > 0 and len(query) < 6: #TODO: return message that the search terms aren't ok
        profiles = UserProfile.objects.filter(*query).select_related('user').order_by('forum_nickname')
    
    output = []
    for profile in profiles:
        label = profile.forum_nickname
        output.append({
            "id": profile.user.id,
            "label": label,
            "value": ''
        })
    return HttpResponse(json.dumps(output))
