# Generated by Django 3.2.24 on 2024-02-26 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0006_auto_20221227_1158"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="registrationquestion",
            name="answers",
        ),
        migrations.RemoveField(
            model_name="registrationattempt",
            name="answer",
        ),
        migrations.RemoveField(
            model_name="registrationattempt",
            name="question",
        ),
        migrations.DeleteModel(
            name="QuestionAnswer",
        ),
        migrations.DeleteModel(
            name="RegistrationQuestion",
        ),
    ]
