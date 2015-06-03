# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib2
from django.db import models, migrations
import brouwers.forum_tools.fields
import datetime
from django.utils.timezone import utc
from django.conf import settings
import brouwers.albums.models


def save_topic_link(apps, schema_editor):
    Album = apps.get_model('albums', 'Album')
    for album in Album.objects.exclude(build_report=''):
        split = urllib2.urlparse.urlsplit(album.build_report)
        query = urllib2.urlparse.parse_qs(split.query)
        topic = query.get('t')
        if topic is not None:
            album.topic_id = int(topic[0])
            album.save()


def fix_ordering(apps, schema_editor):
    seen_albums = set()
    albums_add = seen_albums.add

    orders = {}

    Photo = apps.get_model('albums', 'Photo')
    for photo in Photo.objects.all():
        album = photo.album_id
        if album not in seen_albums:
            max_order = 1
            albums_add(album)
        orders.setdefault(max_order, [])
        orders[max_order].append(photo.id)
        max_order += 1

    for order, id_list in orders.items():
        Photo.objects.exclude(order=order).filter(id__in=id_list).update(order=order)


class Migration(migrations.Migration):

    replaces = [(b'albums', '0001_initial'), (b'albums', '0002_auto_20150405_2118'), (b'albums', '0003_auto_20150408_0912'), (b'albums', '0004_auto_20150408_0913'), (b'albums', '0005_auto_20150408_0913'), (b'albums', '0003_auto_20150507_2216'), (b'albums', '0006_merge'), (b'albums', '0007_auto_20150520_1948'), (b'albums', '0008_auto_20150520_2152'), (b'albums', '0009_auto_20150522_2023'), (b'albums', '0010_auto_20150603_1149')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'album 05-04-2015', max_length=b'256', verbose_name='album title', db_index=True)),
                ('clean_title', models.CharField(default=b'', max_length=b'256', verbose_name='album title', blank=True)),
                ('description', models.CharField(max_length=500, verbose_name='album description', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('last_upload', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), db_index=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('order', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='order', db_index=True, blank=True)),
                ('public', models.BooleanField(default=True, help_text='Can this album be viewed by everyone? Untick to make the album available only to yourself.', verbose_name='Public?')),
                ('build_report', models.URLField(help_text='Link to the forumtopic of the build.', max_length=500, verbose_name='build report', blank=True)),
                ('votes', models.IntegerField(default=0, verbose_name='appreciation')),
                ('writable_to', models.CharField(default=b'u', max_length=1, verbose_name='writable to', choices=[(b'u', 'owner'), (b'g', 'group'), (b'o', 'everyone')])),
                ('trash', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order', 'title'),
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
                'permissions': (('edit_album', 'Can edit/remove album'), ('see_all_albums', 'Can see all albums'), ('access_albums', 'Can use new albums')),
            },
        ),
        migrations.CreateModel(
            name='AlbumDownload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('failed', models.BooleanField(default=False)),
                ('album', models.ForeignKey(to='albums.Album')),
                ('downloader', models.ForeignKey(help_text='user who downloaded the album', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-timestamp',),
                'verbose_name': 'album download',
                'verbose_name_plural': 'album downloads',
            },
        ),
        migrations.CreateModel(
            name='AlbumGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('album', models.ForeignKey(verbose_name='album', to='albums.Album', help_text='Album for which the group has write permissions.', unique=True)),
                ('users', models.ManyToManyField(help_text='Users who can write in this album.', to=settings.AUTH_USER_MODEL, null=True, verbose_name='users', blank=True)),
            ],
            options={
                'ordering': ('album',),
                'verbose_name': 'album group',
                'verbose_name_plural': 'album groups',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256, verbose_name='name')),
                ('order', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='order', blank=True)),
                ('url', models.URLField(max_length=500, verbose_name='url', blank=True)),
                ('on_frontpage', models.BooleanField(default=False, verbose_name='on frontpage')),
                ('public', models.BooleanField(default=True, help_text="If the category is public, regular users can add their albums to the category. If it isn't, only people with admin permissions can do so.", verbose_name='public')),
            ],
            options={
                'ordering': ['order', 'name'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('width', models.PositiveSmallIntegerField(null=True, verbose_name='width', blank=True)),
                ('height', models.PositiveSmallIntegerField(null=True, verbose_name='height', blank=True)),
                ('image', models.ImageField(height_field=b'height', upload_to=brouwers.albums.models.get_image_path, width_field=b'width', max_length=200, verbose_name='image')),
                ('description', models.CharField(max_length=500, verbose_name='photo description', blank=True)),
                ('uploaded', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('views', models.PositiveIntegerField(default=0)),
                ('order', models.PositiveSmallIntegerField(default=1, null=True, db_index=True, blank=True)),
                ('trash', models.BooleanField(default=False)),
                ('album', models.ForeignKey(to='albums.Album')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['album', 'order', 'pk'],
                'verbose_name': 'Photo',
                'verbose_name_plural': 'Photos',
            },
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_img_size', models.PositiveSmallIntegerField(default=0, help_text='Your pictures will be scaled to this size.', verbose_name='default image dimensions', choices=[(0, b'1024x768'), (1, b'800x600'), (2, b'1024x1024'), (3, b'800x800')])),
                ('default_uploader', models.CharField(default=b'F', help_text='Multiple files at once makes use of a Flash uploader,\nyou select all your files without having to click too much buttons.\nThe basic uploader has a file field for each image.', max_length=1, verbose_name='default uploader', choices=[(b'F', 'Multiple files at once'), (b'H', 'Basic')])),
                ('auto_start_uploading', models.BooleanField(default=False, help_text='Start upload automatically when files are selected', verbose_name='start uploading automatically?')),
                ('show_direct_link', models.BooleanField(default=False, verbose_name='Show direct links under the photo')),
                ('apply_admin_permissions', models.BooleanField(default=False, help_text='When checked, you will see all the albums and be able to edit them.')),
                ('collapse_sidebar', models.BooleanField(default=True, help_text='Show the sidebar as closed when typing a post.', verbose_name='collapse sidebar')),
                ('hide_sidebar', models.BooleanField(default=False, help_text='Hide the sidebar completely when typing a post and activate it with a button.', verbose_name='hide sidebar')),
                ('sidebar_bg_color', models.CharField(default=b'black', choices=[(b'black', 'Black'), (b'white', 'White'), (b'EEE', 'Light grey'), (b'333', 'Dark grey')], max_length=7, blank=True, help_text='Background for the overlay in the board.', verbose_name='sidebar background color')),
                ('sidebar_transparent', models.BooleanField(default=True, verbose_name='transparent background?')),
                ('text_color', models.CharField(help_text='Text color in the overlay. HTML color format #xxxxxx or #xxx.', max_length=7, verbose_name='sidebar text color', blank=True)),
                ('width', models.CharField(help_text="Width of the sidebar. E.g. '30%' or '300px'.", max_length=6, verbose_name='sidebar width', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'ordering': ('user',),
                'verbose_name': 'User preferences',
                'verbose_name_plural': 'User preferences',
            },
        ),
        migrations.AddField(
            model_name='album',
            name='category',
            field=models.ForeignKey(default=1, blank=True, to='albums.Category', null=True, verbose_name='category'),
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='cover', blank=True, to='albums.Photo', help_text='Image to use as album cover.', null=True, verbose_name='cover'),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('user', 'title')]),
        ),
        migrations.AddField(
            model_name='album',
            name='topic',
            field=brouwers.forum_tools.fields.ForumToolsIDField(type=b'topic', null=True, verbose_name='build report topic', blank=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(default=b'', max_length=b'256', verbose_name='album title', db_index=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='writable_to',
            field=models.CharField(default=b'u', help_text='Specify who can upload images in this album', max_length=1, verbose_name='writable to', choices=[(b'u', 'owner'), (b'g', 'group'), (b'o', 'everyone')]),
        ),
        migrations.RunPython(
            code=save_topic_link,
        ),
        migrations.RunPython(
            code=fix_ordering,
        ),
        migrations.RemoveField(
            model_name='album',
            name='build_report',
        ),
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=b'256', verbose_name='album title', db_index=True),
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='apply_admin_permissions',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='default_img_size',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='default_uploader',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='show_direct_link',
        ),
        migrations.AlterField(
            model_name='albumgroup',
            name='album',
            field=models.OneToOneField(verbose_name='album', to='albums.Album', help_text='Album for which the group has write permissions.'),
        ),
        migrations.AlterField(
            model_name='albumgroup',
            name='users',
            field=models.ManyToManyField(help_text='Users who can write in this album.', to=settings.AUTH_USER_MODEL, verbose_name='users', blank=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
