# Generated by Django 5.0.4 on 2024-05-07 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vacation", "0004_wisata_gambar_utama"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wisata",
            name="alamat",
            field=models.TextField(),
        ),
    ]
