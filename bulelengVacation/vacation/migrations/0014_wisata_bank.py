# Generated by Django 5.0.4 on 2024-08-13 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vacation", "0013_reservasiwisata"),
    ]

    operations = [
        migrations.AddField(
            model_name="wisata",
            name="bank",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
