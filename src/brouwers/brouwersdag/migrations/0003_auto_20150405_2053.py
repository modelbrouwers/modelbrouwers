# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('brouwersdag', '0002_auto_20150405_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='showcasedmodel',
            name='owner',
            field=models.ForeignKey(verbose_name='brouwer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exhibitor',
            name='brouwersdag',
            field=models.ForeignKey(blank=True, to='brouwersdag.Brouwersdag', null=True),
            preserve_default=True,
        ),
        migrations.AlterOrderWithRespectTo(
            name='exhibitor',
            order_with_respect_to='brouwersdag',
        ),
    ]
