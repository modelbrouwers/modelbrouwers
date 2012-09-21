from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.shortcuts import redirect
from brouwers.general.models import UserProfile
from brouwers.general.shortcuts import render_to_response
from models import *
from brouwers.albums.models import Album

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
                album.save()
            except ValidationError:
                pass
    return render_to_response(request, 'migration/albums.html', {'new_albums': new_albums})
