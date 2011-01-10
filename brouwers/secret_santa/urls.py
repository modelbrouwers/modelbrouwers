from django.conf.urls.defaults import *
from models import Participant
from datetime import date

urlpatterns = patterns('brouwers.secret_santa.views',
	(r'^do_lottery', 'lottery'),
	(r'^receiver', 'receiver'),
)

#GENERIC VIEWS
info = {
	'queryset': Participant.objects.filter(year = date.today().year).order_by('pk'),
	'template_name': 'secret_santa/base.html',
	'template_object_name': 'participants'
	}

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^$', 'object_list', info)
    )
