from django.conf.urls import url

from .views import SearchView

app_name = "builds"

urlpatterns = [
    url(r"^search/", SearchView.as_view(), name="search"),
]
