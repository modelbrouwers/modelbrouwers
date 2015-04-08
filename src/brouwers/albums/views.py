from zipfile import ZipFile
import os
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q, Max, Count
from django.forms import ValidationError
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from brouwers.awards.models import Nomination
from brouwers.utils.views import LoginRequiredMixin
from .models import *
from .forms import *
from .utils import resize, admin_mode, can_switch_admin_mode, get_default_img_size


class IndexView(ListView):
    queryset = Album.objects.for_index()
    template_name = 'albums/index.html'
    context_object_name = 'albums'
    paginate_by = 12

    def get_awards_winners(self):
        awards_winners = Nomination.objects.winners()
        try:
            awards_winners = random.sample(awards_winners, 3)
        except ValueError:  # sample greater than population, use entire set
            pass
        return awards_winners

    def get_context_data(self, **kwargs):
        # spotlight: awards winners, select 3 random categories
        # kwargs['awards_winners'] = self.get_awards_winners()
        kwargs['latest_uploads'] = Photo.objects.select_related('user').filter(
                                       album__public=True).order_by('-uploaded')[:20]
        return super(IndexView, self).get_context_data(**kwargs)


class UploadView(LoginRequiredMixin, TemplateView):
    template_name = 'albums/upload.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.album_set.exists():
            messages.warning(request, _('You need to create an album before you can upload photos'))
            return redirect(reverse('albums:create'))
        return super(UploadView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = UploadForm(self.request)
        return super(UploadView, self).get_context_data(**kwargs)


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = CreateAlbumForm
    template_name = 'albums/create.html'
    success_url = reverse_lazy('albums:upload')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AlbumCreateView, self).form_valid(form)


class AlbumDetailView(ListView, SingleObjectMixin):
    paginate_by = 24
    object = None  # SingleObjectMixin
    context_object_name = 'photos'
    template_name = 'albums/album_detail.html'

    def get_album(self):
        if self.object is None:
            self.object = self.get_object(queryset=self.get_album_queryset())
        return self.object

    def get_album_queryset(self):
        qs = Album.objects.public()
        if self.request.user.is_authenticated():
            groups = self.request.user.albumgroup_set.all()
            qs2 = Album.objects.filter(Q(user=self.request.user) | Q(albumgroup__in=groups))
            return (qs | qs2).distinct()
        return qs

    def get_queryset(self):
        """
        Fetch the album from the url and retrieve the photo_set to build the
        list view.
        """
        return self.get_album().photo_set.filter(trash=False)

    def get_context_data(self, **kwargs):
        kwargs['album'] = self.get_album()
        return super(AlbumDetailView, self).get_context_data(**kwargs)





###########################
#        MANAGING         #
###########################
@login_required
def manage(request, album_id=None):
    """
        Manage albums: change the order, delete albums, create a new album.
    """
    AlbumFormSet = modelformset_factory(
            Album, fields=('title', 'description', 'build_report'),
            extra=0, can_order=True,
            can_delete=True
        )
    albums = Album.objects.filter(user=request.user, trash=False)

    if album_id: #fallback pure http (no AJAX)
        album = get_object_or_404(Album, pk=album_id)
    else:
        album = None

    if request.method == "POST":
        add_album_form = AlbumForm(user=request.user)
        if 'add' in request.POST:
            add_album_form = AlbumForm(request.POST, instance=album, user=request.user)
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

        album_formset = AlbumFormSet(queryset=albums) #FIXME: create a special form class for this, add class to certain fields etc.
        if 'manage' in request.POST:
            album_formset = AlbumFormSet(request.POST)
            if album_formset.is_valid():
                for form in album_formset.ordered_forms:
                    form.instance.order = form.cleaned_data['ORDER'] or 1
                    form.instance.save()
                for form in album_formset.deleted_forms:
                    form.instance.trash = True
                    form.instance.clean_title=form.instance.title
                    form.instance.title = "trash_%s_%s" % (timezone.now().strftime('%d%m%Y_%H.%M.%s'), form.instance.title)
                    form.instance.save()
                return HttpResponseRedirect(reverse(manage))
    else:
        if not album:
            album = Album(user=request.user)
        add_album_form = AlbumForm(instance=album, user=request.user)
        # creating a formset to change the ordering of the albums - AJAX degradable
        album_formset = AlbumFormSet(queryset=albums)
    return render(request, 'albums/manage.html', {'albumformset': album_formset, 'add_album_form': add_album_form})

@login_required
def edit_album(request, album_id=None):
    q = Q(pk=album_id)
    if not admin_mode(request.user):
        q = Q(q, user=request.user)

    album = get_object_or_404(Album, q)
    from django.forms.models import inlineformset_factory
    GroupFormset = inlineformset_factory(Album, AlbumGroup, extra=1)

    if request.method == "POST":
        form = EditAlbumForm(request.POST, instance=album, user=request.user)
        formset = GroupFormset(request.POST, instance=album)
        if form.is_valid():
            form.save()
            response = HttpResponseRedirect(reverse(my_albums_list))
            if formset.is_valid() and album.writable_to == 'g':
                formset.save()
                return response
            elif not formset.is_valid():
                pass
            else:
                return response
    else:
        form = EditAlbumForm(instance=album, user=request.user)
        formset = GroupFormset(instance=album)
    return render(request, 'albums/edit_album.html', {'form': form, 'formset': formset})

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
def edit_photo(request, photo_id=None):
    q = Q(pk=photo_id)
    if not admin_mode(request.user):
        q = Q(q, user=request.user)

    photo = get_object_or_404(Photo, q)
    if request.method == "POST":
        form = EditPhotoForm(request.user, request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(browse_album, args=[photo.album.id]))
    else:
        form = EditPhotoForm(request.user, instance=photo)
    return render(request, 'albums/edit_photo.html', {'form': form})

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

def albums_list(request):
    user = request.user
    if user.has_perm('albums.see_all_albums') or user.has_perm('albums.edit_album'):
        q = Q(trash=False)
    else:
        q = Q(trash=False, public=True)
    albums = Album.objects.select_related('user').filter(q).order_by('-last_upload')

    p = Paginator(albums, 30)
    page = request.GET.get('page', 1)
    try:
        albums = p.page(page)
    except (PageNotAnInteger, TypeError):
        albums = p.page(1)
    except EmptyPage:
        albums = p.page(p.num_pages)

    needs_closing_tag_row = False
    if len(albums) % 5 != 0:
        needs_closing_tag_row = True

    searchform = SearchForm()
    return render(request, 'albums/list.html', {
            'albums': albums,
            'needs_closing_tag_row': needs_closing_tag_row,
            'searchform': searchform
            })

def browse_album(request, album_id=None):
    q = Q(pk=album_id)
    if request.user.is_authenticated():
        groups = request.user.albumgroup_set.all()
        if not admin_mode(request.user):
            q = Q(q, Q(public=True) | Q(user=request.user) | Q(albumgroup__in=groups))
    else:
        q = Q(q, public=True)
    album = get_object_or_404(Album, q, trash=False)
    # increment album views
    album.views = F('views') + 1
    album.save()
    album = get_object_or_404(Album, pk=album_id)

    photos = album.photo_set.filter(trash=False)
    p = Paginator(photos, 32)

    page = request.GET.get('page', 1)
    try:
        photos = p.page(page)
    except (PageNotAnInteger, TypeError):
        # If page is not an integer, deliver first page.
        photos = p.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        photos = p.page(p.num_pages)

    needs_closing_tag_row = False
    if len(photos) % 4 != 0:
        needs_closing_tag_row = True
    return render(request, 'albums/browse_album.html',
        {'album': album, 'photos': photos, 'needs_closing_tag_row': needs_closing_tag_row}
        )

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

def photo(request, photo_id=None):
    q = Q(pk=photo_id, album__trash=False)
    if request.user.is_authenticated():
        if not admin_mode(request.user):
            groups = request.user.albumgroup_set.all()
            q = Q(q, Q(album__public=True) | Q(user=request.user) | Q(album__albumgroup__in=groups))
    else:
        q = Q(q, album__public=True)
    photo = get_object_or_404(Photo, q)
    photo.views = F('views') + 1
    photo.save()
    photo = get_object_or_404(Photo, pk=photo_id)
    return render(request, 'albums/photo.html', {'photo': photo})
