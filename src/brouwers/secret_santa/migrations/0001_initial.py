# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Couple',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ['secret_santa', 'user__username'],
                'verbose_name': 'participant',
                'verbose_name_plural': 'participants',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecretSanta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveSmallIntegerField(help_text='Year the lottery starts.', unique=True, verbose_name='year')),
                ('enrollment_start', models.DateTimeField(help_text='From when can people enroll.', verbose_name='enrollment start')),
                ('enrollment_end', models.DateTimeField(help_text='Until when can people enroll.', verbose_name='enrollment end')),
                ('lottery_date', models.DateTimeField(help_text='When will the lottery happen?', verbose_name='lottery date')),
                ('lottery_done', models.BooleanField(default=False, verbose_name='Lottery done?')),
                ('price_class', models.PositiveSmallIntegerField(help_text='Enter a value here for the estimated price class of the gift.', null=True, verbose_name='price class', blank=True)),
            ],
            options={
                'ordering': ['-year'],
                'verbose_name': 'secret santa',
                'verbose_name_plural': 'secret santas',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='participant',
            name='secret_santa',
            field=models.ForeignKey(verbose_name='secret santa edition', to='secret_santa.SecretSanta', null=True),
            preserve_default=True,
        ),
    ]
