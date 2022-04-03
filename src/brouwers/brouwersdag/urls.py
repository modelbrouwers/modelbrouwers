from django.urls import path

from . import views

app_name = "brouwersdag"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("sign-up/", views.SignupView.as_view(), name="model-signup"),
    path(
        "sign-up/<int:pk>/cancel/",
        views.CancelSignupView.as_view(),
        name="cancel-signup",
    ),
    path("my-models/", views.MyModelsView.as_view(), name="my-models"),
    path("my-models/<int:pk>/", views.EditModelView.as_view(), name="edit-model"),
    path("models/<int:pk>/", views.GoToBuildReportView.as_view(), name="model-detail"),
    path("print/", views.PrintSignupsView.as_view(), name="print-signups"),
]
