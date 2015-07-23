# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urlparse

from django.db import IntegrityError, migrations, transaction


def copy_kit_data(apps, schema_editor):
    Build = apps.get_model('builds', 'Build')
    ModelKit = apps.get_model('kits', 'ModelKit')
    Scale = apps.get_model('kits', 'Scale')

    for build in Build.objects.all():

        # translate the topic url to the topic FK
        if build.topic_id:
            build.forum_topic_id = build.topic_id

        elif build.url:
            url = urlparse.urlparse(build.url)
            querydict = urlparse.parse_qs(url.query)
            _id = querydict.get('t', None)
            if _id is not None:
                build.forum_topic_id = int(_id[0])

        if build.scale and build.brand:
            scale, _ = Scale.objects.get_or_create(scale=build.scale)
            kit, _ = ModelKit.objects.get_or_create(
                scale=scale, brand=build.brand, name=build.title.strip(),
                defaults={'submitter_id': 1}
            )
            build.kit = kit
        elif build.scale:
            pass
        elif build.brand:
            scale, _ = Scale.objects.get_or_create(scale=0)
            kit, _ = ModelKit.objects.get_or_create(
                scale=scale, brand=build.brand, name=build.title,
                defaults={'submitter_id': 1}
            )
            build.kit = kit

        with transaction.atomic():
            try:
                build.save()
            except IntegrityError:
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0006_auto_20150723_2016'),
    ]

    operations = [
        migrations.RunPython(copy_kit_data)
    ]
