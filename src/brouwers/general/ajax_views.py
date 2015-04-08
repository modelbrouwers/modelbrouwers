import json

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic.base import View

from brouwers.general.decorators import login_required_403
from .models import UserProfile, Announcement


@login_required_403
def search_users(request):
    inputresults = request.GET.__getitem__('term').split(' ')
    query = []
    for value in inputresults:
        q = Q(forum_nickname__icontains=value) | \
            Q(user__first_name__icontains=value) | \
            Q(user__last_name__icontains=value)
        query.append(q)
    if len(query) > 0 and len(query) < 6:  # TODO: return message that the search terms aren't ok
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


class AnnouncementView(View):
    def get(self, request, *args, **kwargs):
        data = {'html': None}
        announcement = Announcement.objects.get_current()
        if announcement is not None:
            data['html'] = announcement.text
        return HttpResponse(json.dumps(data), content_type="application/json")
