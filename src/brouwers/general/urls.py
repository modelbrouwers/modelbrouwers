from django.conf.urls import patterns, url
from .views import ServeHbsTemplateView
from .ajax_views import AnnouncementView

urlpatterns = patterns(
    'brouwers.general.views',
    url(r'^$', 'index', name='index'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^templates/(?P<app_name>\w+)/(?P<template_name>[\w\-_]+)/$',
        ServeHbsTemplateView.as_view(),
        name='hbs_template')  # get handlebars templates
)


# AJAX
urlpatterns += patterns(
    'brouwers.general.ajax_views',
    url(r'^user/search/$',    'search_users'),
    url(r'^utils/get-announcement/', AnnouncementView.as_view(), name='get-announcement'),
)
