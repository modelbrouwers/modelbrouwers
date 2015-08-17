# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.translation import ugettext_lazy as _

from djchoices import DjangoChoices, ChoiceItem


class Backgrounds(DjangoChoices):
    black = ChoiceItem('black', _('Black'))
    white = ChoiceItem('white', _('White'))
    grey = ChoiceItem('EEE', _('Light grey'))
    dark_grey = ChoiceItem('333', _('Dark grey'))


def validate_backgrounds(value):
    return Backgrounds.validator(value)


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0001_squashed_0010_auto_20150603_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='sidebar_bg_color',
            field=models.CharField(default=b'black', choices=[(b'black', 'Black'), (b'white', 'White'), (b'EEE', 'Light grey'), (b'333', 'Dark grey')], max_length=7, validators=[validate_backgrounds], help_text='Background for the overlay in the board.', verbose_name='sidebar background color'),
        ),
    ]
