# Generated by Django 4.1.4 on 2022-12-26 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sitemy", "0003_alter_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="videos",
            name="videofile",
            field=models.FileField(
                blank=True, null=True, upload_to="videos/", verbose_name=""
            ),
        ),
    ]
