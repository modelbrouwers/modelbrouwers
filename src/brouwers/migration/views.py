import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from brouwers.albums.models import Album, Photo

from .models import *
from .forms import PhotoMigrationForm

User = get_user_model()


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'migration/base.html')


@user_passes_test(lambda u: u.is_superuser)
def albumusers(request):
    if request.method == 'POST':
        emails = request.POST.getlist('emails')
        for email in emails:
            AlbumUserMigration.objects.filter(email=email).delete()
        ids = request.POST.getlist('migrations')
        AlbumUserMigration.objects.filter(id__in=ids).delete()
        return redirect(reverse(albumusers))
    else:
        emails = AlbumUserMigration.objects.exclude(email__icontains=".nl").exclude(email__icontains=".be").values_list('email', flat=True).order_by('email')
        data = {}
        for email in emails:
            data[email] = AlbumUserMigration.objects.filter(email=email).order_by('username')
    return render(request, 'migration/albumusers.html', {'data': data})


@user_passes_test(lambda u: u.is_superuser)
def find_django_user(request):
    migrations = AlbumUserMigration.objects.filter(django_user=None).order_by('username')
    total = migrations.count()
    found = 0
    for migration in migrations:
        username = migration.username.replace(" ", "_")
        users = User.objects.filter(username=username)
        if not users:
            users = User.objects.filter(email=migration.email).exclude(email='')
        if users:
            migration.django_user = users[0]
            key = 'link%s' % migration.id
            if key in request.POST and request.POST[key] == 'on':
                migration.save()
            found += 1
    return render(request, 'migration/albumusers.html', {'migrations': migrations, 'total': total, 'found': found})


@user_passes_test(lambda u: u.is_superuser)
def migrate_albums(request):
    albums = AlbumMigration.objects.filter(migrated=False)
    new_albums = []
    for album in albums:
        django_user = album.owner.django_user
        if django_user:
            new_album = Album(
                title = album.title,
                description = album.description,
                user = django_user
            )
            try:
                new_album.full_clean()
                new_album.save()
                new_albums.append(new_album)
                album.migrated = True
                album.new_album = new_album
                album.save()
            except ValidationError:
                pass
    return render(request, 'migration/albums.html', {'new_albums': new_albums})


@user_passes_test(lambda u: u.is_superuser)
def migrate_pictures(request):
    p = None
    failed_migrations = []

    if request.method == "POST":
        form = PhotoMigrationForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            pictures = PhotoMigration.objects.filter(album__migrated=True, migrated=False).exclude(owner__django_user=None).select_related('album', 'album__new_album', 'owner', 'owner__django_user')[start:end]
            p = []
            albums = []

            import unicodedata
            for picture in pictures:
                album = picture.album.new_album
                user = picture.owner.django_user
                if album and user:
                    if picture.title:
                        description = picture.title
                    else:
                        description = ''
                    if picture.caption:
                        if description:
                            description += ' %s' % picture.caption
                        else:
                            description = picture.caption
                    if len(description) > 500:
                        description = description[:500]

                    # media/albums/<userid>/<albumid>/filename
                    base = "albums/%(userid)s/%(albumid)s/%(filename)s"
                    cleaned_filename = ''.join((c for c in unicodedata.normalize('NFD', picture.filename) if unicodedata.category(c) != 'Mn'))
                    filepath = base % {
                        'userid': user.id,
                        'albumid': album.id,
                        'filename': cleaned_filename
                    }
                    filepath2 = base % {
                        'userid': user.id,
                        'albumid': album.id,
                        'filename': "thumb_" + cleaned_filename
                    }

                    src = "/home/modelbrouw/domains/modelbrouwers.nl/public_html/albums/coppermine/albums/" + picture.filepath + cleaned_filename
                    src2 = "/home/modelbrouw/domains/modelbrouwers.nl/public_html/albums/coppermine/albums/" + picture.filepath + "thumb_" + cleaned_filename
                    #src = settings.MEDIA_ROOT + 'albums/test.jpg'
                    #src2 = settings.MEDIA_ROOT + 'albums/thumb_test.jpg'
                    target = settings.MEDIA_ROOT + filepath
                    target2 = settings.MEDIA_ROOT + filepath2

                    try:
                        if not os.path.lexists(target):
                            if not os.path.isdir(os.path.dirname(target)):
                                os.makedirs(os.path.dirname(target))

                            os.symlink(src, target)
                            os.symlink(src2, target2)
                    except UnicodeEncodeError:
                        failed_migrations.append({
                            'id': picture.id,
                            'filename': picture.filepath + picture.filename,
                            'cleaned_filename': cleaned_filename,
                            'new_filename': filepath
                        })

                    new_photo = Photo(
                        user = user,
                        album = album,
                        width = picture.pwidth,
                        height = picture.pheight,
                        image = filepath,
                        description = description
                    )
                    new_photo.save()
                    picture.migrated = True
                    picture.save()
                    p.append(new_photo)
                    if album not in albums:
                        albums.append(album)

            for album in albums:
                # order in orde zetten
                i = 1
                for photo in album.photo_set.all():
                    photo.order = i
                    photo.save()
                    i += 1
    else:
        form = PhotoMigrationForm()

    cnt = PhotoMigration.objects.filter(album__migrated=True, migrated=False).exclude(owner__django_user=None).count()
    return render(request, 'migration/photos.html', {'photos': p, 'form': form, 'count': cnt, 'failed_migrations': failed_migrations})
