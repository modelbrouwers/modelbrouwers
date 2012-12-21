from django.conf.urls.defaults import *

urlpatterns = patterns('shirts.views',
    (r'^$', 'index'),
    )
