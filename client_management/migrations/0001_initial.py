# Generated by Django 4.2.1 on 2023-12-06 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
    ]
