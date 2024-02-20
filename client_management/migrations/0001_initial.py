# Generated by Django 4.2.1 on 2024-02-19 11:37

from django.conf import settings
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
            name='AddClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(max_length=13)),
                ('alternate_number', models.CharField(blank=True, max_length=13, null=True)),
                ('email_id', models.EmailField(max_length=254)),
                ('reference', models.CharField(choices=[('1', 'google'), ('2', 'Facebook'), ('3', 'Website'), ('4', 'Previous Client'), ('5', 'Other')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_car', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(blank=True, max_length=200, null=True)),
                ('usercar', models.CharField(blank=True, max_length=200, null=True)),
                ('cartype', models.CharField(blank=True, max_length=200, null=True)),
                ('addprofile', models.DateTimeField(auto_now_add=True)),
                ('mobile_number', models.CharField(blank=True, max_length=50, null=True)),
                ('addfavoritedriver', models.ManyToManyField(blank=True, null=True, to='driver_management.adddriver')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('useraddress1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client_management.address')),
            ],
        ),
    ]
