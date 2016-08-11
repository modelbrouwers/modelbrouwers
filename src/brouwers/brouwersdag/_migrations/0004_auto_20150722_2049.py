# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brouwersdag', '0003_auto_20150603_1149'),
        ('kits', '0002_auto_20150722_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showcasedmodel',
            name='brand',
            field=models.ForeignKey(verbose_name='brand', blank=True, to='kits.Brand', null=True),
        ),
    ]
