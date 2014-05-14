from django.db.models import F, Q, Max
from django.conf import settings
# from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import mark_safe
import django.utils.simplejson as json


from general.decorators import login_required_403
from models import *
from forms import PickOwnAlbumForm
from utils import admin_mode

@login_required_403
def get_photos(request, album_id=None):
    q_group = Q(albumgroup__in = request.user.albumgroup_set.all())
    album = get_object_or_404(Album, Q(pk=album_id), Q(Q(user=request.user) | q_group ))
    photos = Photo.objects.filter(album=album, trash=False).order_by('-uploaded')
    return render(request, 'albums/ajax/forum/album_photos.html', {'photos': photos})

@login_required_403
def get_sidebar(request):
    form = PickOwnAlbumForm(request.user)
    return render(request, 'albums/ajax/forum/sidebar.html', {'form': form})

@login_required_403
def get_sidebar_options(request):
    p = Preferences.get_or_create(request.user)
    options = {}
    options['collapse'] = p.get('collapse_sidebar')
    options['hide'] = p.get('hide_sidebar')
    options['transparent'] = p.get('sidebar_transparent')
    options['text_color'] = p.get('text_color')
    options['background_color'] = p.get('sidebar_bg_color')
    options['width'] = p.get('width')
    return HttpResponse(json.dumps(options))

def is_beta_tester(request):
    user = request.user
    if user.has_perm('albums.access_albums'):
        return HttpResponse(1)
    return HttpResponse(0)

@login_required_403
def search(request):
    inputresults = request.GET.__getitem__('term').split(' ')
    query = []
    for value in inputresults:
        q = Q(title__icontains=value) | Q(description__icontains=value)
        query.append(q)
    if len(query) > 0 and len(query) < 10:
        albums = Album.objects.filter(user=request.user, trash=False, *query).order_by('title')
    else:
        return HttpResponse()

    output = []
    for album in albums:
        label = album.__unicode__()
        output.append({
            "album_id": album.id,
            "label": label,
            "value": album.__unicode__(),
        })
    return HttpResponse(json.dumps(output))
