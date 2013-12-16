from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import NominationView

urlpatterns = patterns('awards.views',
    (r'^vote/$', 'vote'),
    (r'^vote/overview/$', 'vote_overview'),
    (r'^vote/scores/$', 'scores'),
    (r'^categories/$', 'category'),
    (r'^categories/(\d+)/$', 'category_list_nominations'),
    (r'^winners/$', 'winners'),
    )

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'awards/base.html'}, name='awards_index'),
    )

urlpatterns += patterns('',
    url(r'^nomination/', login_required(NominationView.as_view()), name='add_nomination'),
)