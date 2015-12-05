# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-05 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_auto_20151205_2025'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Redirect',
        ),
        migrations.DeleteModel(
            name='SoftwareVersion',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='allow_sharing',
            field=models.BooleanField(default=False, help_text="Checking this gives us permission to share your topics and albums on social media. Uncheck if you don't want to share.", verbose_name='allow social sharing'),
        ),
        migrations.AlterUniqueTogether(
            name='passwordreset',
            unique_together=set([]),
        ),
    ]
