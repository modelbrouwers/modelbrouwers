# Generated by Django 2.2.16 on 2020-10-01 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kitreviews", "0003_auto_20160908_1740"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Categorie",
        ),
        migrations.DeleteModel(
            name="Fabrikant",
        ),
        migrations.DeleteModel(
            name="Kit",
        ),
        migrations.DeleteModel(
            name="Review",
        ),
        migrations.DeleteModel(
            name="Reviewer",
        ),
        migrations.DeleteModel(
            name="Uitbreiding",
        ),
    ]
