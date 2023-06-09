# Generated by Django 4.2.1 on 2023-06-01 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("client_management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlaceBooking",
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
                ("from_date", models.DateField()),
                ("to_date", models.DateField()),
                ("no_of_days", models.PositiveIntegerField()),
                ("start_time", models.TimeField()),
                ("coupon_code", models.CharField(blank=True, max_length=15, null=True)),
                (
                    "religion",
                    models.CharField(
                        choices=[
                            ("1", "Hindu"),
                            ("2", "Muslim"),
                            ("3", "Christian"),
                            ("4", "Sikh"),
                        ],
                        max_length=10,
                    ),
                ),
                ("visiting_location", models.CharField(max_length=20)),
                (
                    "request_type",
                    models.CharField(
                        choices=[("1", "Normal"), ("2", "Guest")], max_length=15
                    ),
                ),
                (
                    "trip_type",
                    models.CharField(
                        choices=[("1", "One Way"), ("2", "Round")], max_length=15
                    ),
                ),
                (
                    "client_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="client_management.addclient",
                    ),
                ),
            ],
        ),
    ]
