# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0003_auto_20150723_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preferences',
            name='collapse_sidebar',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='hide_sidebar',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='sidebar_bg_color',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='sidebar_transparent',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='text_color',
        ),
        migrations.RemoveField(
            model_name='preferences',
            name='width',
        ),
        migrations.AddField(
            model_name='preferences',
            name='paginate_by_sidebar',
            field=models.SmallIntegerField(default=25, verbose_name='sidebar number of photos per page', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
