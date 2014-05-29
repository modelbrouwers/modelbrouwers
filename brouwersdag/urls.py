from django.conf.urls import patterns, url
# from django.contrib.auth.decorators import login_required

import views


urlpatterns = patterns('',
    url('^$', views.IndexView.as_view(), name='index'),
    url('^sign-up/$', views.SignupView.as_view(), name='model-signup'),
)
