# Generated by Django 4.2.10 on 2024-03-04 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kitreviews", "0004_auto_20201001_1447"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kitreview",
            name="properties",
            field=models.ManyToManyField(
                blank=True,
                related_name="+",
                through="kitreviews.KitReviewPropertyRating",
                to="kitreviews.kitreviewproperty",
            ),
        ),
    ]
