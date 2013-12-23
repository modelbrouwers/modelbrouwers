from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

from .views import CategoryListView, NominationView, NominationListView, WinnersView

urlpatterns = patterns('awards.views',
    url(r'^vote/$', 'vote', name='vote'),
    (r'^vote/overview/$', 'vote_overview'),
    (r'^vote/scores/$', 'scores'),
    (r'^winners/$', 'winners'),
    )

urlpatterns += patterns('',
    url(r'^$', TemplateView.as_view(template_name='awards/base.html'), name='awards_index'),
    url(r'^categories/$', CategoryListView.as_view(), name='category-list'),
    url(r'^categories/(?P<pk>\d+)/$', NominationListView.as_view()),
    url(r'^categories/(?P<slug>[\w0-9\-_]+)/$', NominationListView.as_view(), name='nominations-list'),
    url(r'^nomination/', login_required(NominationView.as_view()), name='add_nomination'),
    url(r'^winners/(?P<year>\d{4})/$', WinnersView.as_view(), name='winners'),
)