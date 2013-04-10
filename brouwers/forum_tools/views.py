from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.cache import cache_page
from general.utils import get_username_for_user
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

def get_chat(request):
    t = get_template('chat.html')
    if request.user.is_authenticated():
        nickname = get_username_for_user(request.user)
    else:
        nickname = settings.IRC_DEFAULT_NICK
    
    c = Context({
        'MIBBIT_SETTINGS': settings.MIBBIT_SETTINGS,
        'IRC_SERVER': settings.IRC_SERVER,
        'IRC_CHANNEL': settings.IRC_CHANNEL,
        'nickname': nickname,
    })
    
    html = t.render(c)
    json_data = {
        'html': html,
        'title': "Brouwers chat [%s, %s]" % (settings.IRC_SERVER, settings.IRC_CHANNEL)
    }
    return HttpResponse(json.dumps(json_data), mimetype='application/json')
