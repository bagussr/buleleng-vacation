# Generated by Django 5.0.4 on 2024-08-12 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auths", "0005_customuser_domisili"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_agency",
            field=models.BooleanField(default=False),
        ),
    ]
