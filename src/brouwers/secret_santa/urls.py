from django.conf.urls import url

from .views import index, enroll, lottery, receiver

urlpatterns = [
    url(r'^$', index),
    url(r'^enroll/$', enroll),
    url(r'^do_lottery/$', lottery),
    url(r'^receiver/$', receiver),
]
