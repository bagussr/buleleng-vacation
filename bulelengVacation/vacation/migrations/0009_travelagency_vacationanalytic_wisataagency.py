# Generated by Django 5.0.4 on 2024-05-27 12:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vacation", "0008_wisata_pilihan"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TravelAgency",
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
                ("nama", models.CharField(max_length=255)),
                ("kontak", models.CharField(max_length=100)),
                ("alamat", models.TextField()),
                ("deskripsi", models.TextField(blank=True, null=True)),
                ("logo", models.ImageField(upload_to="agency/")),
                ("website", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="VacationAnalytic",
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
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wisata",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vacation.wisata",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WisataAgency",
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
                (
                    "agency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vacation.travelagency",
                    ),
                ),
                (
                    "wisata",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vacation.wisata",
                    ),
                ),
            ],
        ),
    ]
