from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from models import ForumLinkBase
from datetime import date
import json

#@login_required
@cache_page(60*60*24)
def get_sync_data(request):
    response_data = {}
    t = date.today()
    links_to_be_synced = ForumLinkBase.objects.filter(enabled=True, to_date__gte=t, from_date__lte=t)
    for link in links_to_be_synced:
        response_data[link.link_id] = [l.link_id for l in link.forumlinksynced_set.all()]
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
