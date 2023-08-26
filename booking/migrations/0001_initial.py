# Generated by Django 4.2.1 on 2023-08-26 12:24

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('driver_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookinguser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile_number', models.CharField(max_length=14)),
                ('city', models.CharField(blank=True, choices=[('Mumbai', 'Mumbai'), ('Navi Mumbai', 'Navi Mumbai'), ('Thane', 'Thane'), ('Pune', 'Pune'), ('Bangaluru', 'Bangaluru'), ('Delhi', 'Delhi')], default='Mumbai', max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_type', models.CharField(blank=True, max_length=50, null=True)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('currunt_location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=453)),
                ('car_type', models.CharField(max_length=100, null=True)),
                ('gear_type', models.CharField(max_length=100, null=True)),
                ('pickup_location', models.CharField(max_length=100, null=True)),
                ('drop_location', models.CharField(max_length=100, null=True)),
                ('booking_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_favourite', models.BooleanField(default=False)),
                ('invoice_generate', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='driver_management.adddriver')),
                ('placebooking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.placebooking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.bookinguser')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('descriptions', models.CharField(blank=True, max_length=300, null=True)),
                ('ratingdate', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
