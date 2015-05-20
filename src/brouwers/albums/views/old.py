from zipfile import ZipFile
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from django.forms import ValidationError
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import ugettext as _

from ..models import *
from ..forms import *
from ..utils import resize, admin_mode, can_switch_admin_mode, get_default_img_size


@login_required
def download_album(request, album_id=None):
    """
    view generates zip and then redirects to the static page
    let apache handle the file serving
    """
    album = get_object_or_404(Album, pk=album_id)

    #previous downloads: does the file have to be generated?
    last_upload = album.last_upload
    downloads = AlbumDownload.objects.filter(album=album, timestamp__gte=last_upload, failed=False).count()

    #log download
    album_download = AlbumDownload(album=album, downloader=request.user)

    rel_path = os.path.join('albums', str(album.user_id), str(album.id), '{0}.zip'.format(album.id))

    if downloads == 0:
        photos = album.photo_set.filter(trash=False)
        if photos.count() > 0:
            #create zip file
            filename = os.path.join(settings.MEDIA_ROOT, rel_path)
            zf = ZipFile(filename, mode='w')
            try:
                for photo in photos:
                    f = photo.image.path
                    arcname = os.path.split(f)[1]
                    zf.write(f, arcname)
            except:
                album_download.failed = True
            finally:
                zf.close()
        else:
            album_download.failed = True
            album_download.save()
            messages.warning(request, _("This album could not be downloaded because it has no photos yet."))
            return HttpResponseRedirect(reverse(browse_album, args=[album.id]))

    url = '{0}albums/{1}/{2}/{2}.zip'.format(settings.MEDIA_URL, album.user_id, album.id)
    album_download.save()
    return HttpResponseRedirect(url)


@login_required
def preferences(request):
    p, created = Preferences.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = PreferencesForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('albums:index'))
    else:
        form = PreferencesForm(instance=p)
        if not can_switch_admin_mode(request.user):
            del form.fields["apply_admin_permissions"]
    return render(request, 'albums/preferences.html', {'form': form})


###########################
#        BROWSING         #
###########################


@login_required
def my_last_uploads(request):
    last_uploads = Photo.objects.filter(user=request.user, trash=False).order_by('-uploaded')
    p = Paginator(last_uploads, 20)

    page = request.GET.get('page', 1)
    try:
        uploads = p.page(page)
    except (PageNotAnInteger, TypeError):
        # If page is not an integer, deliver first page.
        uploads = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        uploads = p.page(p.num_pages)
    amount = len(uploads.object_list)

    needs_closing_tag_row = False
    if amount < 20 and amount % 5 != 0:
        needs_closing_tag_row = True
    return render(request, 'albums/my_last_uploads.html', {'uploads': uploads, 'needs_closing_tag_row': needs_closing_tag_row})


@login_required
def my_albums_list(request):
    trash = request.GET.get('trash', False)
    extra_parameters = ''
    if trash:
        extra_parameters = '&trash=%s' % trash

    number_to_display = 20
    base_albums = Album.objects.filter(trash=trash)
    own_albums = base_albums.filter(user=request.user, writable_to='u')
    own_public_albums = base_albums.filter(Q(writable_to='o') | Q(writable_to='g'), user=request.user).order_by('order')
    groups = request.user.albumgroup_set.all()
    other_albums = base_albums.filter(Q(writable_to='o') | Q(albumgroup__in=groups)).exclude(user=request.user).distinct()

    albums_list = [own_albums, own_public_albums, other_albums]
    page_keys = ['page_own', 'page_pub', 'page_other']
    albums_data = []

    for albums in albums_list:
        amount = albums.count()
        page_key = page_keys.pop(0)

        show_all = str(request.GET.get('all', False))
        if show_all == '1' and page_key == 'page_own':
            number_to_display = amount

        paginator = Paginator(albums, number_to_display)
        page = request.GET.get(page_key, 1)
        try:
            albums = paginator.page(page)
        except PageNotAnInteger:
            albums = paginator.page(1)
        except EmptyPage:
            albums = paginator.page(paginator.num_pages)

        closing_tag = False
        if amount < number_to_display and amount % 4 != 0:
            closing_tag = True
        albums_data.append(
            {'albums': albums, 'closing_tag': closing_tag}
        )
    new_album = Album(user=request.user)
    form = AlbumForm(instance=new_album, user=request.user)
    return render(request, 'albums/my_albums_list.html', {'albums_data': albums_data, 'trash': trash, 'extra_parameters': extra_parameters, 'form': form})
