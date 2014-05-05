from django.conf.urls import patterns, url

urlpatterns = patterns('shirts.views',
    url(r'^$', 'index'),
)
