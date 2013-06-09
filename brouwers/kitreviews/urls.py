from django.conf.urls.defaults import *

urlpatterns = patterns('kitreviews.views',
    url(r'^$',          'index',        name='index'),
    url(r'^add/$',      'add_review',   name='add_review'),
    url(r'^find_kit/$', 'find_kit',     name='find_kit'),
    )