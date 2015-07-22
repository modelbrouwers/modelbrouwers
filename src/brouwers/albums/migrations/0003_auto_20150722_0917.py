# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0002_auto_20150608_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='writable_to',
            field=models.CharField(default=b'u', help_text='Specify who can upload images in this album', max_length=1, verbose_name='writable to', choices=[(b'u', 'owner'), (b'o', 'everyone')]),
        ),
    ]
