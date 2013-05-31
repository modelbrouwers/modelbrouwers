from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.translation import ungettext as _n
from django.views.decorators.cache import cache_page


from general.utils import get_username_for_user, get_username
from models import ForumLinkBase, Report, ForumPostCountRestriction, ForumUser
from forms import ForumForm
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

@permission_required('forum_tools.can_see_reports')
def get_mod_data(request):
    data = {}
    num_open_reports = Report.objects.filter(report_closed=False).count()
    data['open_reports'] = num_open_reports
    data['text_reports'] = _n("1 open report", "%(num)d open reports", num_open_reports) % {'num': num_open_reports}
    return HttpResponse(json.dumps(data), mimetype="application/json")

@login_required
def get_posting_level(request):
    data = {}
    form = ForumForm(request.GET)
    if form.is_valid():
        forum = form.cleaned_data['forum']
        # forum_user = ForumUser.objects.get(username=get_username(request))
        username = request.user.get_profile().forum_nickname
        forum_user = ForumUser.objects.get(username_clean=username.lower())
        num_posts = forum_user.user_posts

        restrictions = ForumPostCountRestriction.objects.filter(forum=forum)
        data['restrictions'] = [restr.posting_level for restr in restrictions if restr.min_posts > num_posts]
    return HttpResponse(json.dumps(data), mimetype="application/json")