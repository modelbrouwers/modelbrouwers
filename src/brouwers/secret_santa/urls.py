from django.conf.urls import url

from .views import index, enroll, lottery, receiver

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^enroll/$', enroll, name='enroll'),
    url(r'^do_lottery/$', lottery, name='lottery'),
    url(r'^receiver/$', receiver, name='receiver'),
]
