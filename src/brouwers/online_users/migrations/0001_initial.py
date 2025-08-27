from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TrackedUser",
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
                    "last_seen",
                    models.DateTimeField(
                        auto_now=True, verbose_name="last seen online"
                    ),
                ),
                ("tracking_since", models.DateTimeField(auto_now_add=True)),
                (
                    "notificate",
                    models.BooleanField(
                        default=True,
                        help_text="Send a notification to the online moderators when this user is online.",
                        verbose_name="notificate",
                    ),
                ),
            ],
            options={
                "ordering": ("-last_seen",),
                "verbose_name": "tracked user",
                "verbose_name_plural": "tracked users",
            },
            bases=(models.Model,),
        ),
    ]
