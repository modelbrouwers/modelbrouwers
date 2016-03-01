# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('groupbuilds', '0003_auto_20150603_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupbuild',
            name='slug',
            field=autoslug.fields.AutoSlugField(populate_from=b'theme', editable=True, unique=True, verbose_name='slug'),
        ),
    ]
