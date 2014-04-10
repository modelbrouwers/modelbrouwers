from django.conf.urls import patterns, url

urlpatterns = patterns('secret_santa.views',
    url(r'^$',             'index'),
    url(r'^enroll/$',      'enroll'),
    url(r'^do_lottery/$',  'lottery'),
    url(r'^receiver/$',    'receiver'),
)
