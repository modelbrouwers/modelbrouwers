from django.conf.urls import patterns, url

urlpatterns = patterns('kitreviews.views',
    url(r'^$',                      'index',        name='index'),
    url(r'^add/$',                  'add_review',   name='add_review'),
    url(r'^find_kit/$',             'find_kit',     name='find_kit'),
    url(r'^kit/$',                  'kit_detail'),
    url(r'^kit/(\d+)/$',            'kit_detail',   name='kit_detail'), #TODO: switch to generic view maybe
    url(r'^kit/(\d+)/add_review/$', 'add_review', name='kit_add_review'),
)