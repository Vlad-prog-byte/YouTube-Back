# Generated by Django 4.1.4 on 2023-01-15 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sitemy", "0010_profile_ismanager"),
    ]

    operations = [
        migrations.AddField(
            model_name="videos",
            name="isPublished",
            field=models.BooleanField(default=False, verbose_name="Опубликовано ли"),
        ),
    ]
