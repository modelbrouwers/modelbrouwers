from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Max
from django.forms import ValidationError
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

from brouwers.general.shortcuts import render_to_response
from models import *
from forms import *
from utils import resize

###########################
#          BASE           #
###########################
def index(request):
    last_uploads = Photo.objects.filter(album__public=True).order_by('-uploaded')
    amount_last_uploads = last_uploads.count()
    if  amount_last_uploads < 20 and amount_last_uploads % 5 != 0:
        needs_closing_tag_row = True
    else:
        last_uploads = last_uploads[:20]
        needs_closing_tag_row = False
    return render_to_response(request, 'albums/base.html', {'last_uploads': last_uploads, 'needs_closing_tag_row': needs_closing_tag_row})

###########################
#        MANAGING         #
###########################
@login_required
def manage(request, album_id=None):
    """
        Manage albums: change the order, delete albums, create a new album.
    """
    AlbumFormSet = modelformset_factory(
            Album, fields=('title',),
            extra=0, can_order=True,
            can_delete=True
        )
    albums = Album.objects.filter(user=request.user, trash=False)
    
    if album_id: #fallback pure http (no AJAX)
        album = get_object_or_404(Album, pk=album_id)
    else:
        album = None
    
    if request.method == "POST":
        add_album_form = AlbumForm()
        if 'add' in request.POST:
            add_album_form = AlbumForm(request.POST, instance=album)
            if add_album_form.is_valid():
                album = add_album_form.save(commit=False)
                album.user = request.user
                try:
                    album.validate_unique()
                    album.save()
                    return HttpResponseRedirect(reverse(manage))
                except ValidationError:
                    error = u"You already have an album with this title"
                    add_album_form._errors["title"] = add_album_form.error_class([error])
        
        album_formset = AlbumFormSet(queryset=albums)
        if 'manage' in request.POST:
            album_formset = AlbumFormSet(request.POST)
            if album_formset.is_valid():
                for form in album_formset.ordered_forms:
                    form.instance.order = form.cleaned_data['ORDER'] or 1
                    form.instance.save()
                for form in album_formset.deleted_forms:
                    form.instance.trash = True
                    form.instance.title = "trash_%s" % form.instance.title
                    #avoid title-user collisions in the future TODO can still happen, find a fix
                    form.instance.save()
                return HttpResponseRedirect(reverse(manage))
    else:
        add_album_form = AlbumForm(instance=album)
        # creating a formset to change the ordering of the albums - AJAX degradable
        album_formset = AlbumFormSet(queryset=albums)
    return render_to_response(request, 'albums/manage.html', {'albumformset': album_formset, 'add_album_form': add_album_form})

@login_required
def preferences(request):
    p = Preferences.get_or_create(request.user)    
    if request.method == "POST":
        form = PreferencesForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(index))
    else:
        form = PreferencesForm(instance=p)
    return render_to_response(request, 'albums/preferences.html', {'form': form})

###########################
#        UPLOADING        #
###########################
@login_required
def uploadify(request):
    albumform = PickAlbumForm(request.user)
    return render_to_response(request, 'albums/uploadify.html', {'albumform': albumform, 'session_cookie_name': settings.SESSION_COOKIE_NAME, 'session_key': request.session.session_key})

@login_required
def upload(request):
    """
    Pure HTTP based upload, if you don't want to or can't use Flash and/or javascript.
    """
    amountform = AmountForm(request.GET)
    if amountform.is_valid():
        amount = amountform.cleaned_data['amount'] or 20
    else:
        amount = 20
    PhotoFormSet = modelformset_factory(Photo, fields=('image',), extra=amount)
    
    if request.method == "POST":
        albumform = PickAlbumForm(request.user, request.POST)
        formset = PhotoFormSet(request.POST, request.FILES)
        if albumform.is_valid() and formset.is_valid():
            album = albumform.cleaned_data['album']
            photo_ids = []
            max_order = Photo.objects.filter(album=album).aggregate(Max('order'))['order__max'] or 0
            order = max_order + 1
            path = 'albums/%s/%s/' % (request.user.id, album.id)
            # get the resizing dimensions from the preferences
            preferences = Preferences.get_or_create(request.user)
            resize_dimensions = preferences.get_default_img_size()
            i = 0 # to access the file in request.FILES
            for form in formset:
                if form.has_changed():
                    instance = form.save(commit=False)
                    instance.user, instance.album = request.user, album
                    instance.order = order
                    img = request.FILES['form-%s-image' % i]
                    img_data = resize(img, upload_to=path, sizes_data=[resize_dimensions])
                    for data in img_data:
                        instance.width = data[1]
                        instance.height = data[2]
                        instance.image = data[0]
                        instance.save()
                    photo_ids.append(instance.id)
                    order += 1
                i += 1
                #make it a GET request again to pass it to the next function
            request.method = "GET"
            return set_extra_info(request, photo_ids, album, reverse=upload)
    else:
        albumform = PickAlbumForm(request.user)
        formset = PhotoFormSet(queryset=Photo.objects.none())
    return render_to_response(request, 'albums/upload.html', {'amountform': amountform, 'albumform': albumform, 'formset': formset})

@login_required
def pre_extra_info_uploadify(request):
    albumform = PickAlbumForm(request.user, request.GET)
    if albumform.is_valid():
        album = albumform.cleaned_data['album']
        ids_string = request.GET['photo_ids']
        # clean this string, verify these are integers
        ids_list = ids_string[:-1].split(' ')
        photo_ids = []
        for entry in ids_list:
            try:
                photo_ids.append(int(entry))
            except ValueError: # entry is not an integer!
                pass #fail silently
        return set_extra_info(request, photo_ids, album, reverse=uploadify)
    return HttpResponse() #URL is created in javascript, so the form should always validate

#@login_required #bug related to outputting instead of redirecting
def set_extra_info(request, photo_ids=None, album=None, reverse=upload):
    PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=0)
    if request.method == "POST": # editing
        formset = PhotoFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save()
            try:
                a_id = instances[0].album.id
            except IndexError:
                a_id = ''
            return HttpResponseRedirect('/albums/my_gallery/last_uploads/')
            #return HttpResponseRedirect('/albums/photos/?album=%s' % (a_id)) #apparently there's a bug which makes that 'reverse' doesn't work... very odd
    else:
        if not photo_ids:
            return HttpResponseRedirect(reverse('/albums/upload/'))
        p = Photo.objects.filter(id__in = photo_ids, user=request.user) # avoid being ablo to edit someone else's photos
        formset = PhotoFormSet(queryset=p)
        photos_uploaded_now = p.count()
        all_photos_album = album.photo_set.count()
        photos_before = all_photos_album - photos_uploaded_now
    return render_to_response(request, 'albums/extra_info_uploads.html', {'formset': formset, 'photos_before': photos_before, 'album': album})

###########################
#        BROWSING         #
###########################
@login_required
def my_last_uploads(request):
    last_uploads = Photo.objects.filter(user=request.user).order_by('-uploaded')
    p = Paginator(last_uploads, 20)
    
    page = request.GET.get('page')
    try:
        uploads = p.page(page)
    except PageNotAnInteger, TypeError:
        # If page is not an integer, deliver first page.
        uploads = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        uploads = p.page(p.num_pages)
    amount = len(uploads.object_list)
    
    needs_closing_tag_row = False
    if amount < 20 and amount % 5 != 0:
        needs_closing_tag_row = True
    return render_to_response(request, 'albums/my_last_uploads.html', {'uploads': uploads, 'needs_closing_tag_row': needs_closing_tag_row})

@login_required
def photos(request): #TODO: veel uitgebreider maken met deftige pagina's :) is temporary placeholder
    albumform = PickAlbumForm(request.user, request.GET, browse=True)
    if albumform.is_valid():
        album = albumform.cleaned_data['album']
        photos = Photo.objects.filter(user=request.user, album=album)
    else:
        photos = Photo.objects.filter(user=request.user)
    return render_to_response(request, 'albums/photos.html', {'photos': photos, 'albumform': albumform})

@login_required
def my_albums_list(request):
    own_albums = Album.objects.filter(user=request.user)
    other_albums = Album.objects.filter(writable_to='o', public=True)
    return render_to_response(request, 'albums/my_albums_list.html', {'own_albums': own_albums, 'other_albums': other_albums})
