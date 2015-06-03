# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banning', '0002_ban_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ban',
            name='ip',
            field=models.GenericIPAddressField(help_text='Ip address to ban.', null=True, verbose_name='ip', blank=True),
        ),
    ]
