# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0008_auto_20150520_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferences',
            name='apply_admin_permissions',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='default_img_size',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='default_uploader',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='show_direct_link',
        ),
    ]
