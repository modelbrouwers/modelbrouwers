from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q, Max
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404

from brouwers.general.shortcuts import render_to_response
from models import *
from forms import *
from utils import resize

def index(request):
	return render_to_response(request, 'albums/base.html')

@login_required
def manage(request, album_id=None):
	AlbumFormSet = modelformset_factory(
			Album, fields=('title',),
			extra=0, can_order=True,
			can_delete=True
		)
	albums = Album.objects.filter(user=request.user, writable_to="u", trash=False)
	#fallback pure http (no AJAX)
	if album_id:
		album = get_object_or_404(Album, pk=album_id)
	else:
		album = None
	
	if request.method == "POST":
		if 'add' in request.POST:
			add_album_form = AlbumForm(request.POST, instance=album)
			if add_album_form.is_valid():
				album = add_album_form.save(commit=False)
				album.user = request.user
				album.save()
				return HttpResponseRedirect(reverse(manage))
		else:
			add_album_form = AlbumForm()
		
		if 'manage' in request.POST:
			album_formset = AlbumFormSet(request.POST)
			if album_formset.is_valid():
				for form in album_formset.ordered_forms:
					form.instance.order = form.cleaned_data['ORDER'] or 1
					form.instance.save()
				for form in album_formset.deleted_forms:
					form.instance.trash = True
					form.instance.save()
				return HttpResponseRedirect(reverse(manage))
		else:
			album_formset = AlbumFormSet(queryset=albums)
	else:
		add_album_form = AlbumForm(instance=album)
		# creating a formset to change the ordering of the albums
		# AJAX degradable
		album_formset = AlbumFormSet(queryset=albums)
	
	return render_to_response(request, 'albums/manage.html', {'albumformset': album_formset, 'add_album_form': add_album_form})

@login_required
def upload(request):
	amountform = AmountForm(request.GET)
	if amountform.is_valid():
		amount = amountform.cleaned_data['amount'] or 20
		#TODO: fetch the initial album value
	else:
		amount = 20
	PhotoFormSet = modelformset_factory(Photo, fields=('image',), extra=amount)
	
	if request.method == "POST":
		albumform = PickAlbumForm(request.user, request.POST)
		formset = PhotoFormSet(request.POST, request.FILES)
		if albumform.is_valid() and formset.is_valid():
			album = albumform.cleaned_data['album']
			photo_ids = []
			max_order = Photo.objects.filter(album=album).aggregate(Max('order'))['order__max']
			order = max_order + 1
			for form in formset:
				if form.has_changed():
					instance = form.save(commit=False)
					instance.user, instance.album = request.user, album
					instance.order = order
					instance.save()
					photo_ids.append(instance.id)
					order += 1
			#make it a GET request again to pass it to the next function
			request.method = "GET"
			return set_extra_info(request, photo_ids, album)
	else:
		albumform = PickAlbumForm(request.user)
		formset = PhotoFormSet(queryset=Photo.objects.none())
	return render_to_response(request, 'albums/upload.html', {'amountform': amountform, 'albumform': albumform, 'formset': formset})

@login_required
def upload_flash(request):
    albumform = PickAlbumForm(request.user)
    return render_to_response(request, 'albums/uploadify.html', {'albumform': albumform, 'session_cookie_name': settings.SESSION_COOKIE_NAME, 'session_key': request.session.session_key})

@login_required
def set_extra_info(request, photo_ids=None, album=None):
	PhotoFormSet = modelformset_factory(Photo, form=PhotoForm, extra=0)
	if request.method == "POST":
		formset = PhotoFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return HttpResponseRedirect('/albums/') #TODO:change to the album that's being uploaded to
	else:
		if not photo_ids:
			return HttpResponseRedirect(reverse(upload))
		photos = Photo.objects.filter(id__in = photo_ids)
		formset = PhotoFormSet(queryset=photos)
	photos_uploaded_now = len(photo_ids)
	all_photos_album = album.photo_set.count()
	photos_before = all_photos_album - photos_uploaded_now
	return render_to_response(request, 'albums/extra_info_uploads.html', {'formset': formset, 'photos_before': photos_before, 'album': album})

@login_required
def uploadify(request):
    # Processing of each uploaded image
    albumform = PickAlbumForm(request.user, request.POST)
    if albumform.is_valid():
        album = albumform.cleaned_data['album']
        img = request.FILES['Filedata']
        path = 'albums/%s/%s/' % (request.user.id, album.id) #/media/albums/userid/albumid/<img>.jpg
        img_data = resize(img, upload_to=path)
        for data in img_data:
            photo = Photo(user=request.user, album=album, width=data[1], height=data[2])
            photo.image = data[0]
            photo.save()
        return HttpResponse('True', mimetype="text/plain")
    else:
        return HttpResponse()

@login_required
def photos(request):
	photos = Photo.objects.exclude(image__icontains='1024_').exclude(image__icontains='thumb_')
	return render_to_response(request, 'albums/photos.html', {'photos': photos})
