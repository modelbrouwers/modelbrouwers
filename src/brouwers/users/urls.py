from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy

from .forms.auth import PasswordResetForm
from .views import (
    DataDownloadFileView,
    LoginView,
    LogoutView,
    PasswordChangedView,
    ProfileView,
    RegistrationView,
    RequestDataDownloadView,
    UserProfileDetailView,
)

app_name = "users"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("users/<int:pk>/", UserProfileDetailView.as_view(), name="detail"),
    # password reset
    path(
        "password/",
        PasswordChangeView.as_view(
            template_name="users/change_password.html",
            success_url=reverse_lazy("users:change_pw_ok"),
        ),
        name="change_pw",
    ),
    path("password/ok/", PasswordChangedView.as_view(), name="change_pw_ok"),
    path(
        "password/reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:login"),
            form_class=PasswordResetForm,
        ),
        name="pw_reset",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:login"),
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path("data-download/", RequestDataDownloadView.as_view(), name="data-download"),
    path(
        "data-download/<int:pk>/download/",
        DataDownloadFileView.as_view(),
        name="data-download-file",
    ),
]
