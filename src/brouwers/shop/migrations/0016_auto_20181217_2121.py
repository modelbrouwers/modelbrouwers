# Generated by Django 1.11.15 on 2018-12-17 20:21


import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0015_auto_20181209_1936"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("open", "Open"), ("paid", "Paid")],
                        max_length=10,
                        verbose_name="status",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "cart", "verbose_name_plural": "carts",},
        ),
        migrations.CreateModel(
            name="CartProduct",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.PositiveIntegerField(default=1, verbose_name="amount"),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_products",
                        to="shop.Cart",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_products",
                        to="shop.Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "cart product",
                "verbose_name_plural": "cart products",
            },
        ),
        migrations.CreateModel(
            name="CustomerGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="name")),
                (
                    "discount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=3,
                        verbose_name="discount",
                    ),
                ),
            ],
            options={
                "verbose_name": "customer group",
                "verbose_name_plural": "customer groups",
            },
        ),
        migrations.AlterField(
            model_name="productreview",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="shop.Product",
            ),
        ),
    ]
