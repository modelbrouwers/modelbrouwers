from django.urls import path

from .views import SearchView

app_name = "builds"

urlpatterns = [
    path("search/", SearchView.as_view(), name="search"),
]
