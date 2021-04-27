from django.urls import path
from django.views.generic import RedirectView, TemplateView

from .views import WinnersView

app_name = "awards"

urlpatterns = [
    path("", TemplateView.as_view(template_name="awards/landing.html"), name="index"),
    path("hall-of-fame/", WinnersView.as_view(), name="winners"),
    path("hall-of-fame/<int:year>/", WinnersView.as_view(), name="winners"),
    # old redirect URLs, keep them for SEO
    path(
        "winners/", RedirectView.as_view(pattern_name="awards:winners", permanent=True)
    ),
    path(
        "winners/<int:year>/",
        RedirectView.as_view(pattern_name="awards:winners", permanent=True),
    ),
]
