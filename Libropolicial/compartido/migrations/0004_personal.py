# Generated by Django 5.0.6 on 2025-01-06 11:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("compartido", "0003_codigopolicialtol_codigossecundariostol_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Personal",
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
                    "legajo",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        unique=True,
                        verbose_name="Legajo Personal",
                    ),
                ),
                (
                    "dni",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        unique=True,
                        verbose_name="DNI",
                    ),
                ),
                (
                    "telefono",
                    models.CharField(
                        blank=True, max_length=15, null=True, verbose_name="Teléfono"
                    ),
                ),
                (
                    "domicilio",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Domicilio"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="personal_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
