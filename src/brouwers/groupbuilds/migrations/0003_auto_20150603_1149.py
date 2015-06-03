# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groupbuilds', '0002_auto_20150405_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupbuild',
            name='participants',
            field=models.ManyToManyField(related_name='groupbuilds', through='groupbuilds.Participant', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
