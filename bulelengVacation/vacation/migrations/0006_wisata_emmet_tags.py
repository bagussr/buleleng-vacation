# Generated by Django 5.0.4 on 2024-05-07 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vacation", "0005_alter_wisata_alamat"),
    ]

    operations = [
        migrations.AddField(
            model_name="wisata",
            name="emmet_tags",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
    ]
