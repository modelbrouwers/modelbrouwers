from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
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

@sensitive_post_parameters()
@login_required
def password_change(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            data = {
                'success': True,
                'msg': {
                    'tag': 'success', 
                    'text': _("Your password was successfully changed.")
                    },
                }
            return HttpResponse(json.dumps(data))
    
    from django.template import RequestContext
    from django.template.loader import get_template
    c = RequestContext(request, {'form': form})
    t = get_template('general/ajax/password_change.html')
    html = t.render(c)
    data = {'success': False, 'html': html}
    return HttpResponse(json.dumps(data))
