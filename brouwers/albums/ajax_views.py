from django.db import IntegrityError
from django.db.models import F, Q, Max
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
import django.utils.simplejson as json

from brouwers.general.shortcuts import render_to_response
from models import *
from forms import AlbumForm, EditAlbumFormAjax, PickAlbumForm, OrderAlbumForm
from utils import resize, admin_mode
import itertools

@login_required
def new_album(request):
    if request.method == "POST": #submission of new album
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            try:
                album.validate_unique()
                album.set_order()
                album.save()
                return HttpResponse("<div title=\"%s\"><input type=\"hidden\" id=\"status\" value=\"%s\"/></div>" % (album.title, album.id))
            except ValidationError:
                error = "You have used this album title before. Make sure you pick an unique title."
    else: #request for rendered form
        form = AlbumForm()
        error = None
    return render_to_response(request, 'albums/ajax/new_album.html', {'form': form, 'error': error})

@login_required
def uploadify(request):
    # Processing of each uploaded image
    albumform = PickAlbumForm(request.user, request.POST)
    
    if albumform.is_valid():
        album = albumform.cleaned_data['album']
        max_order = Photo.objects.filter(album=album).aggregate(Max('order'))['order__max'] or 0
        img = request.FILES['Filedata']
        path = 'albums/%s/%s/' % (request.user.id, album.id) #/media/albums/<userid>/<albumid>/<img>.jpg
        # get the resizing dimensions from the preferences #TODO this might move to utils in the future
        preferences = Preferences.get_or_create(request.user)
        resize_dimensions = preferences.get_default_img_size()
        img_data = resize(img, upload_to=path, sizes_data=[resize_dimensions])
        
        for data in img_data:
            photo = Photo(user=request.user, album=album, width=data[1], height=data[2])
            photo.image = data[0]
            photo.order = max_order + 1
            photo.save()
            p_id = photo.id
        return HttpResponse('%s' % p_id, mimetype="text/plain") #return the photo id
    else:
        return HttpResponse()

### search function
def search(request):
    inputresults = request.GET.__getitem__('term').split(' ')
    query = []
    for value in inputresults:
        q = Q(title__icontains=value) | Q(description__icontains=value) | Q(user__username__icontains=value)
        query.append(q)
    if len(query) > 0 and len(query) < 10:
        if not request.user.is_authenticated() or not admin_mode(request.user):
            query.append(Q(public=True))
        albums = Album.objects.filter(trash=False, *query).order_by('title')
    else:
        return HttpResponse()
    output = []
    for album in albums:
        label = mark_safe(u"%s \u2022 %s" % (album.__unicode__(), album.user.get_profile().forum_nickname))
        output.append({
            "id": album.id,
            "label": label,
            "value": album.__unicode__(),
            "url": album.get_absolute_url()
        })
    return HttpResponse(json.dumps(output))

### set album_cover
@login_required
def set_cover(request):
    if request.method == "POST":
        p_id = request.POST['photo']
        try:
            p_id = int(p_id)
            if admin_mode(request.user):
                photo = get_object_or_404(Photo, pk=p_id)
            else:
                photo = get_object_or_404(Photo, pk=p_id, user=request.user)
            photo.album.cover = photo
            photo.album.save()
            return HttpResponse(1)
        except ValueError: #not an integer
            pass
    return HttpResponse()

@login_required
def reorder(request):
    form = OrderAlbumForm(request.user, request.POST)
    if form.is_valid():
        album = form.cleaned_data['album']
        album_before = form.cleaned_data['album_before']
        album_after = form.cleaned_data['album_after']

        if album_after and album.order > album_after.order: # moved forward
            lower = album_after.order
            upper = album.order
            album.order = lower
            
            albums_to_reorder = Album.objects.filter(order__gte=lower, order__lt=upper)
            albums_to_reorder.update(order=(F('order') + 1))
            album.save()
        
        elif album_before and album_before.order > album.order: # moved backwards
            lower = album.order
            upper = album_before.order
            album.order = upper
            
            albums_to_reorder = Album.objects.filter(order__gt=lower, order__lte=upper)
            albums_to_reorder.update(order=(F('order') - 1))
            album.save()
        
        elif ((album_before and album_before.order == album.order) or (album_after and album_after.order == album.order)):
            order = album.order
            if album_after:
                albums_to_reorder = Album.objects.filter(order__gte=order, title__gt=album.title)
                albums_to_reorder.update(order=(F('order') + 1))
            elif album_before:
                album.order = (F('order') + 1)
                albums_to_reorder = Album.objects.filter(order__gte=order, title__gt=album.title)
                albums_to_reorder.update(order=(F('order') + 2))
                album.save()
    return HttpResponse()

@login_required
def get_all_own_albums(request):
    own_albums = Album.objects.filter(user=request.user, writable_to='u', trash=False)
    return render_to_response(request, 'albums/albums_list/albums_rows_li.html', {'albums': own_albums})

@login_required
def edit_album(request):
    if request.method == "POST":
        form = PickAlbumForm(request.user, request.POST)
        if form.is_valid():
            album = form.cleaned_data["album"]
            editform = EditAlbumFormAjax(request.POST, instance=album)
            photos = editform.fields["cover"].queryset
            if editform.is_valid() and (album.user == request.user or admin_mode(request.user)):
                editform.save()
                album = get_object_or_404(Album, pk=album.id);
                return render_to_response(request, 'albums/ajax/album_li.html', {'album': album, 'custom_id': 'temp'})
    else:
        form = PickAlbumForm(request.user, request.GET)
        if form.is_valid():
            album = form.cleaned_data["album"]
            if request.user == album.user or admin_mode(request.user):
                editform = EditAlbumFormAjax(instance=album)
                photos = editform.fields["cover"].queryset
            else:
                return HttpResponse('This event has been logged')
    return render_to_response(request, 'albums/ajax/edit_album.html', {'form': editform, 'photos': photos})

@login_required
def remove_album(request):
    status = 'fail'
    form = PickAlbumForm(request.user, request.POST)
    if form.is_valid():
        album = form.cleaned_data["album"]
        album.trash = True
        album.title = "trash_%s_%s" % (datetime.now().strftime('%d%m%Y_%H.%M.%s'), album.title)
        album.save()
        status = 'ok'
    return HttpResponse(status)

@login_required
def get_title(request):
    title = ''
    form = PickAlbumForm(request.user, request.GET)
    if form.is_valid():
        album = form.cleaned_data["album"]
        title = album.title
    return HttpResponse(title)

@login_required
def restore_album(request):
    form = PickAlbumForm(request.user, request.POST, trash=True)
    if form.is_valid():
        album = form.cleaned_data["album"]
        album.trash = False
        album.title = album.clean_title
        
        i = itertools.count(2)
        saved = False
        while(not saved):
            try:
                album.save()
                saved = True
                return HttpResponse('ok')
            except IntegrityError:
                album.title = "%s_%s" % (album.clean_title, i.next())
            
            print i
    return HttpResponse('<table>'+form.as_table()+'</table>')
