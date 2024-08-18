# Generated by Django 5.0.4 on 2024-08-12 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("judul", models.CharField(max_length=255)),
                ("gambar", models.ImageField(upload_to="article/")),
                ("content", models.TextField()),
                ("created_at", models.DateField(auto_now_add=True, null=True)),
            ],
        ),
    ]