from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..models import *
from ..forms import *


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
