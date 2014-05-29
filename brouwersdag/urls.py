from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import views


urlpatterns = patterns('',
    url('^sign-up/$', views.SignupView.as_view(), name='model-signup'),
)
