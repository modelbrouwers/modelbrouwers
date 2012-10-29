from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import redirect
from brouwers.general.models import UserProfile
from brouwers.general.shortcuts import render_to_response
from models import *
from forms import PhotoMigrationForm
from brouwers.albums.models import Album, Photo
import os

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render_to_response(request, 'migration/base.html')

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
    return render_to_response(request, 'migration/albumusers.html', {'data': data})

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
    return render_to_response(request, 'migration/albumusers.html', {'migrations': migrations, 'total': total, 'found': found})

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
    return render_to_response(request, 'migration/albums.html', {'new_albums': new_albums})

@user_passes_test(lambda u: u.is_superuser)
def migrate_pictures(request):
    p = None
    cnt = PhotoMigration.objects.filter(album__migrated=True, migrated=False).count()
    if request.method == "POST":
        form = PhotoMigrationForm(request.POST)
        if form.is_valid():
            import unicodedata
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            pictures = PhotoMigration.objects.filter(album__migrated=True, migrated=False).select_related('album', 'album__new_album', 'owner', 'owner__djang_user')[start:end]
            p = []
            albums = []
            for picture in pictures:
                try:
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
                    
                        src = "/home/modelbrouw/domains/modelbrouwers.nl/public_html/albums/coppermine/albums/" + picture.filepath + picture.filename
                        src2 = "/home/modelbrouw/domains/modelbrouwers.nl/public_html/albums/coppermine/albums/" + picture.filepath + "thumb_" + picture.filename
                        #src = settings.MEDIA_ROOT + 'albums/test.jpg'
                        #src2 = settings.MEDIA_ROOT + 'albums/thumb_test.jpg'
                        target = settings.MEDIA_ROOT + filepath
                        target2 = settings.MEDIA_ROOT + filepath2
                    
                        if not os.path.lexists(target):
                            if not os.path.isdir(os.path.dirname(target)):
                                os.makedirs(os.path.dirname(target))
                            os.symlink(src, target)
                            os.symlink(src2, target2)
                    
                        new_photo = Photo(
                            user = user,
                            album = album,
                            width = picture.pwidth,
                            height = picture.pheight,
                            image = filepath,
                            description = description
                        )
                        try:
                            #new_photo.full_clean()
                            new_photo.save()
                            picture.migrated = True
                            picture.save()
                            p.append(new_photo)
                            if album not in albums:
                                albums.append(album)
                        except ValidationError:
                            pass
                except UnicodeEncodeError: #don't bother
                    pass
            
                for album in albums:
                    # order in orde zetten
                    i = 1
                    for photo in album.photo_set.all():
                        photo.order = i
                        photo.save()
                        i += 1
    else:
        form = PhotoMigrationForm()
    return render_to_response(request, 'migration/photos.html', {'photos': p, 'form': form, 'count':cnt})
