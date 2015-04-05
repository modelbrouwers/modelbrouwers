# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0001_initial'),
        ('general', '0001_initial'),
        ('kitreviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='brand',
            field=models.ForeignKey(verbose_name='brand', blank=True, to='kitreviews.Brand', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='build',
            name='profile',
            field=models.ForeignKey(to='general.UserProfile'),
            preserve_default=True,
        ),
    ]
