from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import password_change

from .views import (ActivationView, LoginView, LogoutView, RegistrationView,
                    ProfileView, UserProfileDetailView, PasswordChangedView)

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(
        r'^activate/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ActivationView.as_view(),
        name='activate'
    ),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^password/$', password_change, {
        'template_name': 'users/change_password.html',
        'post_change_redirect': reverse_lazy('users:change_pw_ok'),
    }, name='change_pw'),
    url(r'^password/ok/$', PasswordChangedView.as_view(), name='change_pw_ok'),
    url(r'^users/(?P<pk>\d+)/$', UserProfileDetailView.as_view(), name='detail'),
)
