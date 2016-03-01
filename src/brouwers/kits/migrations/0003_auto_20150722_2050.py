# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import brouwers.kits.models


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0002_auto_20150722_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='modelkit',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=brouwers.kits.models.get_kit_slug, unique=True, verbose_name='slug'),
        ),
    ]
