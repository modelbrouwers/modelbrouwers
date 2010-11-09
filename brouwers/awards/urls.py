from django.conf.urls.defaults import *

urlpatterns = patterns('brouwers.awards.views',
    (r'^$', 'index'),
    (r'^nomination/$', 'nomination'),
#    (r'^nomination/(\d+)/$', 'nomination_detail'),
    (r'^vote/$', 'vote'),
    (r'^categories/$', 'category'),
    (r'^categories/(\d+)/$', 'category_list_nominations'),
    (r'^login/$', 'custom_login'),
    (r'^logout/$', 'custom_logout'),
    (r'^register/$', 'register'),
    )

