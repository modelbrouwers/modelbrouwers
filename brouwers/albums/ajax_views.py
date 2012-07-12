from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from brouwers.general.shortcuts import render_to_response
from models import *
from forms import *

@login_required
def new_album(request):
    if request.method == "POST": #submission of new album
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user #FIXME verify user and album title uniqueness
            album.save()
            return HttpResponse("<input type=\"hidden\" id=\"status\" value=\"%s\" title=\"%s\"/>" % (album.id, album.title))
    else: #request for rendered form
        form = AlbumForm()
    return render_to_response(request, 'albums/ajax/new_album.html', {'form': form})
