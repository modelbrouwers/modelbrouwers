# Generated by Django 1.11.15 on 2018-09-30 17:47


from django.db import migrations

import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0007_auto_20180930_1917"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                populate_from="name",
                unique=True,
                verbose_name="slug",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug_de",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
                verbose_name="slug",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug_en",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
                verbose_name="slug",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug_nl",
            field=autoslug.fields.AutoSlugField(
                editable=False,
                max_length=200,
                null=True,
                populate_from="name",
                unique=True,
                verbose_name="slug",
            ),
        ),
    ]
