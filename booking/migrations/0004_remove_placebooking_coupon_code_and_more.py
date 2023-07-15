# Generated by Django 4.2.1 on 2023-07-15 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_placebooking_client_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placebooking',
            name='coupon_code',
        ),
        migrations.RemoveField(
            model_name='placebooking',
            name='no_of_days',
        ),
        migrations.RemoveField(
            model_name='placebooking',
            name='religion',
        ),
        migrations.RemoveField(
            model_name='placebooking',
            name='request_type',
        ),
        migrations.RemoveField(
            model_name='placebooking',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='placebooking',
            name='trip_type',
        ),
        migrations.RemoveField(
            model_name='placebooking',
            name='visiting_location',
        ),
        migrations.AddField(
            model_name='placebooking',
            name='car_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='placebooking',
            name='currunt_loaction',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='placebooking',
            name='drop_location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='placebooking',
            name='gear_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='placebooking',
            name='pickup_location',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
