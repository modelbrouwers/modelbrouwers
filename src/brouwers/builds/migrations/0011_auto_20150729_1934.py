# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0010_build_topic_start_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='build',
            options={'ordering': ['kits__scale', 'kits__brand__name'], 'verbose_name': 'build report', 'verbose_name_plural': 'build reports'},
        ),
    ]
