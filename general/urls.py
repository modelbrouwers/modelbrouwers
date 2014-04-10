from django.conf import settings
from django.conf.urls import patterns, url, include
from .views import ServeHbsTemplateView
from .ajax_views import AnnouncementView

urlpatterns = patterns('general.views',
    url(r'^$', 'index', name='index'),
    url(r'^login/$', 'custom_login', name='custom_login'),
    url(r'^logout/$', 'custom_logout'),
    url(r'^register/$', 'register'),
    url(r'^profile/$', 'profile'),
    url(r'^users/(\w+)/$', 'user_profile'),
    url(r'^confirm_account/$', 'confirm_account'),
    url(r'^reset_pw/$', 'password_reset'),
    url(r'^do_reset_pw/$', 'do_password_reset'),
    url(r'^templates/(?P<app_name>\w+)/(?P<template_name>[\w]+)/$', ServeHbsTemplateView.as_view(), name='hbs_template') # get handlebars templates
)

# new auth backend
urlpatterns += patterns('general.views2',
    (r'^new_login/$',     'custom_login'),
    )

# AJAX
urlpatterns += patterns('general.ajax_views',
    (r'^user/search/$',    'search_users'),
    (r'^profile/ajax/change_password/$', 'password_change'),
    url(r'^utils/get-announcement/', AnnouncementView.as_view(), name='get-announcement'),
    )

urlpatterns += patterns('django.contrib.auth.views',
    (r'^profile/change_password/$', 'password_change', {'template_name':'general/password.html'}),
    (r'^password_change_done/$','password_change_done', {'template_name': 'general/password_change_done.html'}),
    )

# API
if 'tastypie' in settings.INSTALLED_APPS:
    from tastypie.api import Api
    from general.api.resources import UserResource

    v1_api = Api(api_name='v1')

    v1_api.register(UserResource())

    urlpatterns += patterns('',
        (r'^api/', include(v1_api.urls)),
        )