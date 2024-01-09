# Generated by Django 4.2.1 on 2024-01-08 05:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('driver_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='driverenquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.BigIntegerField()),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_type', models.CharField(choices=[('1', 'Local'), ('2', 'Outstation'), ('3', 'Drop')], max_length=10)),
                ('date_of_enquiry', models.DateTimeField(default=datetime.datetime.now)),
                ('client_name', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(max_length=15)),
                ('alternate_mobile_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email_id', models.EmailField(blank=True, max_length=254, null=True)),
                ('location', models.CharField(max_length=20)),
                ('duty_hours', models.CharField(choices=[('1', '4 Hours'), ('2', '8 Hours'), ('3', '12 Hours')], max_length=10)),
                ('car_details', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='driver_management.adddriver')),
            ],
        ),
    ]
