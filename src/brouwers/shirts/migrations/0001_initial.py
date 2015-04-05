# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShirtOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.CharField(default=b'L', max_length=4, verbose_name='size', choices=[(b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'XXL', b'XXL'), (b'XXXL', b'XXXL')])),
                ('type', models.CharField(default=b'S', max_length=1, verbose_name='type', choices=[(b'S', 'Standard'), (b'G', 'Girlie')])),
                ('color', models.CharField(default=b'W', max_length=2, verbose_name='color', choices=[(b'W', 'White'), (b'B', 'Black')])),
                ('send_per_mail', models.BooleanField(default=False, help_text='Mailing the shirt will add 3.2 euros to the costs and you need to fill in your address data in your profile.', verbose_name='mail the shirt')),
                ('moderator', models.BooleanField(default=False, help_text='Check this box if you want the moderator shirt. Moderators only!', verbose_name='moderator shirt')),
                ('order_time', models.DateTimeField(auto_now_add=True, verbose_name='order time')),
                ('payment_received', models.BooleanField(default=False, verbose_name='payment received')),
                ('delivered', models.BooleanField(default=False, verbose_name='delivered?')),
            ],
            options={
                'ordering': ('order_time',),
                'verbose_name': 'shirt order',
                'verbose_name_plural': 'shirt orders',
            },
            bases=(models.Model,),
        ),
    ]
