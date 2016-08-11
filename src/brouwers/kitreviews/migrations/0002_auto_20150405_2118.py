# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('albums', '0001_squashed_0010_auto_20150603_1149'),
        ('kitreviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelkit',
            name='submitter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kitreviewvote',
            name='kit_review',
            field=models.ForeignKey(to='kitreviews.KitReview'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kitreviewvote',
            name='voter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='kitreviewvote',
            unique_together=set([('kit_review', 'voter')]),
        ),
        migrations.AddField(
            model_name='kitreview',
            name='album',
            field=models.ForeignKey(verbose_name='album', blank=True, to='albums.Album', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kitreview',
            name='model_kit',
            field=models.ForeignKey(to='kitreviews.ModelKit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kitreview',
            name='reviewer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
