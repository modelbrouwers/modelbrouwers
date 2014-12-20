from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^sign-up/$', views.SignupView.as_view(), name='model-signup'),
    url(r'^sign-up/(?P<pk>\d+)/cancel/$', views.CancelSignupView.as_view(), name='cancel-signup'),
    url(r'^my-models/$', views.MyModelsView.as_view(), name='my-models'),
    url(r'^my-models/(?P<pk>\d+)/$', views.EditModelView.as_view(), name='edit-model'),
    url(r'^models/(?P<pk>\d+)/$', views.GoToBuildReportView.as_view(), name='model-detail'),
    url(r'^print/$', views.PrintSignupsView.as_view(), name='print-signups'),
)
