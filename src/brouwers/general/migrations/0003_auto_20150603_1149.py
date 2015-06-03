# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_auto_20150405_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationattempt',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', db_index=True),
        ),
        migrations.AlterField(
            model_name='registrationquestion',
            name='answers',
            field=models.ManyToManyField(to='general.QuestionAnswer', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='categories_voted',
            field=models.ManyToManyField(to='awards.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
