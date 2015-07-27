# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kitreviews', '0004_auto_20150722_0917'),
        ('kits', '0003_auto_20150722_2050'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
