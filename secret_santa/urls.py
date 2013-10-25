from django.conf.urls.defaults import *
from models import Participant
from datetime import date

urlpatterns = patterns('secret_santa.views',
    (r'^$',             'index'),
    (r'^enroll/$',      'enroll'),
    (r'^do_lottery/$',  'lottery'),
    (r'^receiver/$',    'receiver'),
)
