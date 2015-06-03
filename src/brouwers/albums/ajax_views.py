import json
import urllib2
from urlparse import urlparse

from django.db.models import Max
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.forms.models import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from brouwers.general.decorators import login_required_403
from .models import Album, Photo, Preferences, AlbumGroup
from .forms import AlbumGroupForm, PickAlbumForm, UploadFromURLForm
from .utils import resize, admin_mode, get_default_img_size


GroupFormset = inlineformset_factory(Album, AlbumGroup, form=AlbumGroupForm, extra=1, can_delete=False)


# uploading images from urls
@login_required_403
def upload_url(request):
    albumform = PickAlbumForm(request.user, request.POST)
    urlform = UploadFromURLForm(request.POST)
    if albumform.is_valid() and urlform.is_valid():
        url = urlform.cleaned_data['url']
        album = albumform.cleaned_data['album']
        name = urlparse(url).path.split('/')[-1]

        tmp_img = NamedTemporaryFile(delete=True)
        tmp_img.write(urllib2.urlopen(url).read())
        tmp_img.flush()

        max_order = Photo.objects.filter(album=album).aggregate(Max('order'))['order__max'] or 0
        path = 'albums/%s/%s/' % (request.user.id, album.id)

        photo = Photo(user=request.user, album=album)
        photo.image.save(name, File(tmp_img))
        photo.image.open()

        # get the resizing dimensions from the preferences #TODO this might move to utils in the future
        preferences = Preferences.get_or_create(request.user)
        resize_dimensions = get_default_img_size(preferences)
        img_data = resize(photo.image, upload_to=path, sizes_data=[resize_dimensions], overwrite=True)

        for data in img_data:
            photo.width = data[1]
            photo.height = data[2]
            photo.order = max_order + 1
            photo.save()
            p_id = photo.id
        return HttpResponse(p_id, content_type="text/plain")
    return render(request, 'albums/uploadify_url.html', {'urlform': urlform})


# CLASS BASED VIEWS ###

class RotateView(SingleObjectMixin, View):
    """ View taking a photo, rotating it, and returning the success status when done """
    model = Photo

    def get_queryset(self):
        qs = super(RotateView, self).get_queryset()
        if not admin_mode(self.request.user):
            qs = qs.filter(user=self.request.user)
        return qs

    def post(self, request, *args, **kwargs):
        photo = self.get_object()
        direction = self.request.POST['direction']
        if direction == 'cw':
            photo.rotate_right()
        elif direction == 'ccw':
            photo.rotate_left()
        else:
            response = {'result': 'Invalid direction'}

        response = {'result': 'success', 'ok': True}
        return HttpResponse(json.dumps(response), content_type='application/json')
