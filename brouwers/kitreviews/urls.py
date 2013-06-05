from django.conf.urls.defaults import *

urlpatterns = patterns('kitreviews.views',
    url(r'^$',          'index',    name='index'),
    )