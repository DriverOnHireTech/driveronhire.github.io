# Generated by Django 4.2.1 on 2023-07-31 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adddriver',
            name='member_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='adddriver',
            name='relationship',
            field=models.CharField(max_length=100),
        ),
    ]
