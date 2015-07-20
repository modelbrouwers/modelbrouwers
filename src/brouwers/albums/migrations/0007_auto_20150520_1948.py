# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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

    dependencies = [
        ('albums', '0006_merge'),
    ]

    operations = [
        migrations.RunPython(fix_ordering)
    ]
