from django.conf import settings
from django.conf.urls import patterns, url, include
from .views import ServeHbsTemplateView
from .ajax_views import AnnouncementView

urlpatterns = patterns('brouwers.general.views',
    url(r'^$', 'index', name='index'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^users/(\w+)/$', 'user_profile'),
    url(r'^reset_pw/$', 'password_reset', name='reset-pw'),
    url(r'^do_reset_pw/$', 'do_password_reset'),
    url(r'^templates/(?P<app_name>\w+)/(?P<template_name>[\w]+)/$', ServeHbsTemplateView.as_view(), name='hbs_template') # get handlebars templates
)


# AJAX
urlpatterns += patterns('brouwers.general.ajax_views',
    url(r'^user/search/$',    'search_users'),
    url(r'^profile/ajax/change_password/$', 'password_change'),
    url(r'^utils/get-announcement/', AnnouncementView.as_view(), name='get-announcement'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^profile/change_password/$', 'password_change', {'template_name':'general/password.html'}),
    url(r'^password_change_done/$','password_change_done', {'template_name': 'general/password_change_done.html'}),
)

# API
if 'tastypie' in settings.INSTALLED_APPS:
    from tastypie.api import Api
    from brouwers.general.api.resources import UserResource

    v1_api = Api(api_name='legacy')

    v1_api.register(UserResource())

    urlpatterns += patterns('',
        url(r'^api/', include(v1_api.urls)),
    )
