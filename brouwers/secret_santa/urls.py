from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.secret_santa.views',
	(r'^$', 'index'),
)
