# Generated by Django 4.2.16 on 2024-09-08 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_reco", "0002_song"),
    ]

    operations = [
        migrations.AddField(
            model_name="song",
            name="url",
            field=models.URLField(default="http://example.com"),
        ),
    ]
