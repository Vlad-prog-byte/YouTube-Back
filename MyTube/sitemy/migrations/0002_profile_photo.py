# Generated by Django 4.1.4 on 2022-12-22 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sitemy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="photo",
            field=models.CharField(default=None, max_length=500, verbose_name="Фото"),
        ),
    ]