from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url('^$', views.IndexView.as_view(), name='index'),
    url('^sign-up/$', views.SignupView.as_view(), name='model-signup'),
    url('^sign-up/(?P<pk>\d+)/cancel/$', views.CancelSignupView.as_view(), name='cancel-signup'),
    url('^my-models/$', views.MyModelsView.as_view(), name='my-models'),
    url('^my-models/(?P<pk>\d+)/$', views.EditModelView.as_view(), name='edit-model'),
)
