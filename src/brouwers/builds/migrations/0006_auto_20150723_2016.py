# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0003_auto_20150722_2050'),
        ('builds', '0005_auto_20150723_1921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='kit',
        ),
        migrations.AddField(
            model_name='build',
            name='kits',
            field=models.ManyToManyField(to='kits.ModelKit', verbose_name='kits', blank=True),
        ),
    ]
