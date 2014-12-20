from django.conf.urls import patterns, url

urlpatterns = patterns('brouwers.shirts.views',
    url(r'^$', 'index'),
)
