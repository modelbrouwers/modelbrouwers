# Generated by Django 1.11.20 on 2019-06-29 14:16


import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0021_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="cart",
            field=models.ForeignKey(
                blank=True,
                help_text="The shopping cart that generated this payment.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="shop.Cart",
                verbose_name="shopping cart",
            ),
        ),
    ]
