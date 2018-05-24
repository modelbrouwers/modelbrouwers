from django.conf.urls import url
from django.contrib.auth.views import (
    PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)
from django.urls import reverse_lazy

from .forms.auth import PasswordResetForm
from .views import (
    ActivationView, LoginView, LogoutView, PasswordChangedView, ProfileView,
    RegistrationView, UserProfileDetailView, RequestDataDownloadView
)

app_name = 'users'
urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(
        r'^activate/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ActivationView.as_view(),
        name='activate'
    ),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^users/(?P<pk>\d+)/$', UserProfileDetailView.as_view(), name='detail'),

    # password reset
    url(r'^password/$', PasswordChangeView.as_view(
        template_name='users/change_password.html',
        success_url=reverse_lazy('users:change_pw_ok'),
    ), name='change_pw'),
    url(r'^password/ok/$', PasswordChangedView.as_view(), name='change_pw_ok'),
    url(r'^password/reset/$', PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:login'),
        form_class=PasswordResetForm,
    ), name='pw_reset'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:login'),
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'),

    url(r'^data-download/$', RequestDataDownloadView.as_view(), name='data-download'),
]
