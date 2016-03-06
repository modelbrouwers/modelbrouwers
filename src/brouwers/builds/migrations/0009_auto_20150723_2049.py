# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0008_auto_20150723_2048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='build',
            old_name='forum_topic',
            new_name='topic',
        ),
    ]
