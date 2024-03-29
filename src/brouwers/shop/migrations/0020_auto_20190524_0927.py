# Generated by Django 1.11.20 on 2019-05-24 07:27


from django.db import migrations, models

from brouwers.shop.models.utils import get_max_order


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0019_auto_20190524_0918"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentmethod",
            name="order",
            field=models.PositiveSmallIntegerField(
                default=get_max_order, verbose_name="order"
            ),
        ),
    ]
