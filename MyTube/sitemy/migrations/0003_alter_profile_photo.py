# Generated by Django 4.1.4 on 2022-12-22 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sitemy", "0002_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="photo",
            field=models.CharField(blank=True, max_length=500, verbose_name="Фото"),
        ),
    ]
