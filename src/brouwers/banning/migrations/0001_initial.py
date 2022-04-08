from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ban",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "ip",
                    models.IPAddressField(
                        help_text="Ip address to ban.", verbose_name="ip", blank=True
                    ),
                ),
                (
                    "expiry_date",
                    models.DateTimeField(
                        help_text="Date the ban expires. Leave blank for permabans.",
                        null=True,
                        verbose_name="expiry date",
                        blank=True,
                    ),
                ),
                (
                    "reason_internal",
                    models.TextField(verbose_name="reason (internal)", blank=True),
                ),
                (
                    "reason",
                    models.TextField(
                        help_text="This reason will be shown to the banned user.",
                        verbose_name="reason",
                        blank=True,
                    ),
                ),
                (
                    "automatic",
                    models.BooleanField(
                        default=False, verbose_name="automatically created?"
                    ),
                ),
            ],
            options={
                "verbose_name": "ban",
                "verbose_name_plural": "bans",
            },
            bases=(models.Model,),
        ),
    ]
