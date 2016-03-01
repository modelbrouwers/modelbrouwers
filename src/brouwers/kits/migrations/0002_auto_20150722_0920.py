# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def move_brands(apps, schema_editor):
    OldBrand = apps.get_model('kitreviews', 'Brand')
    Brand = apps.get_model('kits', 'Brand')

    # make sure to flush old instances
    Brand.objects.all().delete()

    for value in OldBrand.objects.values().order_by('id'):
        brand = Brand(**value)
        brand.save()


class Migration(migrations.Migration):

    dependencies = [
        ('kits', '0001_initial'),
        ('kitreviews', '0004_auto_20150722_0917'),
    ]

    operations = [
        migrations.RunPython(code=move_brands)
    ]
