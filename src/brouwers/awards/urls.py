from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import (
    CategoryListView, NominationView, NominationListView,
    VoteView, WinnersView,
    vote_overview,
    scores
)


# app_name = 'awards'
urlpatterns = [
    url(r'^vote/overview/$', vote_overview),
    url(r'^vote/scores/$', scores),
] + [
    url(r'^$', TemplateView.as_view(template_name='awards/base.html'), name='awards_index'),
    url(r'^categories/$', CategoryListView.as_view(), name='category-list'),
    url(r'^categories/(?P<pk>\d+)/$', NominationListView.as_view()),
    url(r'^categories/(?P<slug>[\w0-9\-_]+)/$', NominationListView.as_view(), name='nominations-list'),
    url(r'^nomination/', NominationView.as_view(), name='add_nomination'),
    url(r'^voting/', VoteView.as_view(), name='voting'),
    url(r'^winners/(?P<year>\d{4})/$', WinnersView.as_view(), name='winners'),
    url(r'^winners/$', WinnersView.as_view(), name='winners'),
]
