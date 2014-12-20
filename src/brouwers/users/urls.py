from django.conf.urls import patterns, url

from .views import ActivationView, LoginView, LogoutView, RegistrationView

urlpatterns = patterns('',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^activate/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', ActivationView.as_view(), name='activate'),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
)
