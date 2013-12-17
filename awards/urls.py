from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import NominationView, NominationListView

urlpatterns = patterns('awards.views',
    (r'^vote/$', 'vote'),
    (r'^vote/overview/$', 'vote_overview'),
    (r'^vote/scores/$', 'scores'),
    (r'^categories/$', 'category'),
    (r'^winners/$', 'winners'),
    )

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'awards/base.html'}, name='awards_index'),
    )

urlpatterns += patterns('',
    url(r'^categories/(?P<pk>\d+)/$', NominationListView.as_view(), name='nominations-list'),
    url(r'^nomination/', login_required(NominationView.as_view()), name='add_nomination'),
)