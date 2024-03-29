# Generated by Django 1.11.11 on 2018-04-01 16:58


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="enabled",
            field=models.BooleanField(default=True, verbose_name="enabled"),
        ),
        migrations.AddField(
            model_name="category",
            name="enabled_de",
            field=models.BooleanField(default=True, verbose_name="enabled"),
        ),
        migrations.AddField(
            model_name="category",
            name="enabled_en",
            field=models.BooleanField(default=True, verbose_name="enabled"),
        ),
        migrations.AddField(
            model_name="category",
            name="enabled_nl",
            field=models.BooleanField(default=True, verbose_name="enabled"),
        ),
        migrations.AddField(
            model_name="category",
            name="seo_keyword",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="seo keyword"
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="seo_keyword_de",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="seo keyword"
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="seo_keyword_en",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="seo keyword"
            ),
        ),
        migrations.AddField(
            model_name="category",
            name="seo_keyword_nl",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="seo keyword"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="shop/category/", verbose_name="thumbnail"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=30, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_de",
            field=models.CharField(max_length=30, null=True, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_en",
            field=models.CharField(max_length=30, null=True, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="category",
            name="name_nl",
            field=models.CharField(max_length=30, null=True, verbose_name="name"),
        ),
    ]
