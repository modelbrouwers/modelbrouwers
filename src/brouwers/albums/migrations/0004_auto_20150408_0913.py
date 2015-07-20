# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib2

from django.db import models, migrations


def save_topic_link(apps, schema_editor):
    Album = apps.get_model('albums', 'Album')
    for album in Album.objects.exclude(build_report=''):
        split = urllib2.urlparse.urlsplit(album.build_report)
        query = urllib2.urlparse.parse_qs(split.query)
        topic = query.get('t')
        if topic is not None:
            album.topic_id = int(topic[0])
            album.save()


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0003_auto_20150408_0912'),
    ]

    operations = [
        migrations.RunPython(save_topic_link),
    ]
