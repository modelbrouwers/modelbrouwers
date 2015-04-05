# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('secret_santa', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='couple',
            name='receiver',
            field=models.ForeignKey(related_name='receiver', to='secret_santa.Participant'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='couple',
            name='secret_santa',
            field=models.ForeignKey(verbose_name='secret santa edition', to='secret_santa.SecretSanta', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='couple',
            name='sender',
            field=models.ForeignKey(to='secret_santa.Participant'),
            preserve_default=True,
        ),
    ]
