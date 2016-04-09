# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-06 20:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_auto_20151205_2051'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationquestion',
            name='lang',
            field=models.CharField(choices=[(b'en', 'English'), (b'nl', 'Dutch')], default=b'nl', max_length=10, verbose_name='language'),
        ),
    ]