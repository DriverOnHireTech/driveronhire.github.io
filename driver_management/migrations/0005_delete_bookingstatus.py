# Generated by Django 4.2.1 on 2023-09-15 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('driver_management', '0004_bookingstatus_delete_driverhistory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bookingstatus',
        ),
    ]
