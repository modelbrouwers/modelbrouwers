# Generated by Django 1.11.11 on 2018-04-22 15:12


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_auto_20180419_2006"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"verbose_name": "product", "verbose_name_plural": "products"},
        ),
        migrations.AlterModelOptions(
            name="productbrand",
            options={
                "verbose_name": "product brand",
                "verbose_name_plural": "product brands",
            },
        ),
        migrations.AlterModelOptions(
            name="productmanufacturer",
            options={
                "verbose_name": "product manufacturer",
                "verbose_name_plural": "product manufacturers",
            },
        ),
        migrations.AlterField(
            model_name="product",
            name="vat",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=3, verbose_name="vat"
            ),
        ),
    ]
