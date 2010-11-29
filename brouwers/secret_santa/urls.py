from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.secret_santa.views',
	(r'^$', 'index'),
	(r'^do_lottery', 'lottery'),
	(r'^receiver', 'receiver'),
)
