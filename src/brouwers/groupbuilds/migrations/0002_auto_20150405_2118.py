# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('forum_tools', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groupbuilds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='user',
            field=models.ForeignKey(related_name='gb_participants', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupbuild',
            name='admins',
            field=models.ManyToManyField(help_text='Users who manage the group build.', related_name='admin_groupbuilds', verbose_name='admins', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupbuild',
            name='applicant',
            field=models.ForeignKey(related_name='groupbuilds_applied', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupbuild',
            name='category',
            field=models.ForeignKey(verbose_name='forum category', to='forum_tools.ForumCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupbuild',
            name='participants',
            field=models.ManyToManyField(related_name='groupbuilds', null=True, through='groupbuilds.Participant', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
