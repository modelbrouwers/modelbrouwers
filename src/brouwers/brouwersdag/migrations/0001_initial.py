# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brouwersdag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('date', models.DateField(null=True, verbose_name='date', blank=True)),
            ],
            options={
                'ordering': ('-date',),
                'verbose_name': 'brouwersdag',
                'verbose_name_plural': 'brouwersdagen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('price', models.DecimalField(default=b'0.0', verbose_name='price per model', max_digits=5, decimal_places=2)),
                ('max_num_models', models.PositiveSmallIntegerField(default=0, help_text='Maximum number of models per participant, enter 0 for unlimited.', verbose_name='models per participant')),
                ('max_participants', models.PositiveSmallIntegerField(default=0, help_text='Maximum number of participants, enter 0 for unlimited.', verbose_name='maximum number of participants')),
                ('is_current', models.BooleanField(default=False, help_text='Marking this competition as active will deactivate all other competitions.', verbose_name='current open competition?')),
            ],
            options={
                'verbose_name': 'competition',
                'verbose_name_plural': 'competitions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exhibitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('website', models.URLField(verbose_name='website', blank=True)),
                ('space', models.CharField(help_text='Amount of space needed. 100 characters or less.', max_length=100, verbose_name='space needed', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'exhibitor',
                'verbose_name_plural': 'exhibitors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShowCasedModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner_name', models.CharField(max_length=254, verbose_name='real name')),
                ('email', models.EmailField(max_length=75, verbose_name='e-mail address')),
                ('name', models.CharField(max_length=254, verbose_name='model name')),
                ('scale', models.PositiveSmallIntegerField(help_text='Enter the number after the "1:" or "1/". E.g. 1/48 --> enter 48.', verbose_name='scale')),
                ('remarks', models.TextField(help_text='Add the features that make this model special here, e.g. "scratch built cockpit"', verbose_name='remarkable elements', blank=True)),
                ('topic', models.URLField(verbose_name='topic url', blank=True)),
                ('length', models.PositiveSmallIntegerField(help_text='In cm.', null=True, verbose_name='length', blank=True)),
                ('width', models.PositiveSmallIntegerField(help_text='In cm.', null=True, verbose_name='width', blank=True)),
                ('height', models.PositiveSmallIntegerField(help_text='In cm.', null=True, verbose_name='height', blank=True)),
                ('is_competitor', models.BooleanField(default=False, verbose_name='enter competition?')),
                ('is_paid', models.BooleanField(default=False, verbose_name='competition fee paid?')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='added')),
            ],
            options={
                'verbose_name': 'showcased model',
                'verbose_name_plural': 'showcased models',
            },
            bases=(models.Model,),
        ),
    ]
