from django.conf.urls import url

from .ajax_views import AnnouncementView, search_users
from .views import ServeHbsTemplateView

app_name = 'general'
urlpatterns = [
    url(r'^templates/(?P<app_name>\w+)/(?P<template_name>[\w\-_]+)/$',
        ServeHbsTemplateView.as_view(),
        name='hbs_template'),

    url(r'^user/search/$', search_users),
    url(r'^utils/get-announcement/', AnnouncementView.as_view(), name='get-announcement'),

]
