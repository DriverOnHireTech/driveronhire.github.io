# Generated by Django 4.2.1 on 2023-09-02 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=30, unique=True)),
                ('branch_address', models.CharField(max_length=100)),
                ('branch_pin', models.CharField(max_length=10)),
                ('branch_contact', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Branch',
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_company', models.CharField(max_length=50)),
                ('car_model', models.CharField(max_length=50)),
                ('car_type', models.CharField(max_length=50)),
                ('car_transmission', models.IntegerField(choices=[(1, 'Manual'), (2, 'Automatic'), (3, 'Luxury')])),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Car',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=30, unique=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'City',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=30, unique=True)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Country',
            },
        ),
        migrations.CreateModel(
            name='CouponList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_list', models.IntegerField(choices=[(1, 'Local'), (2, 'Drop'), (3, 'Outstation'), (4, 'Permanent')])),
                ('coupon_name', models.CharField(max_length=50)),
                ('coupon_code', models.CharField(max_length=50)),
                ('discount_amount', models.FloatField()),
                ('use_count', models.IntegerField()),
                ('valid_from', models.DateTimeField()),
                ('valid_till', models.DateTimeField()),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Coupon List',
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_name', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Reference',
            },
        ),
        migrations.CreateModel(
            name='region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_code', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=30, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.country')),
            ],
            options={
                'verbose_name_plural': 'State',
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_name', models.CharField(max_length=50, unique=True)),
                ('gst_rate', models.FloatField()),
                ('cgst', models.FloatField()),
                ('sgst', models.FloatField()),
                ('igst', models.FloatField()),
                ('cess', models.FloatField()),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Tax',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_name', models.CharField(max_length=30, unique=True)),
                ('status', models.BooleanField(default=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.city', to_field='city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.country')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.state', to_field='state')),
            ],
            options={
                'verbose_name_plural': 'Zone',
            },
        ),
        migrations.CreateModel(
            name='ZoneMapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.city', to_field='city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.country')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.state', to_field='state')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.zone', to_field='zone_name')),
            ],
            options={
                'verbose_name_plural': 'Zone Mapping',
            },
        ),
        migrations.CreateModel(
            name='UserMaster',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('password', models.CharField(blank=True, max_length=300, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('email_id', models.EmailField(blank=True, max_length=50, null=True)),
                ('role', models.CharField(blank=True, choices=[('Admin', 'Admin'), ('Temprory', 'Temprory'), ('Permanent', 'Permanent'), ('Recruit', 'Recruit')], null=True)),
                ('status', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.branch', to_field='branch_name')),
            ],
            options={
                'verbose_name_plural': 'User Master',
                'permissions': (('view_UserMaster', 'Can view the UserMaster'), ('can_publish_UserMaster', 'Can publish a UserMaster')),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme_type', models.CharField(max_length=50)),
                ('duty_type', models.IntegerField(choices=[(1, 'Day'), (2, 'Drop'), (3, 'Night'), (4, 'Outstation')])),
                ('car_transmission', models.IntegerField(choices=[(1, 'Manual'), (2, 'Automatic'), (3, 'Luxury')])),
                ('amount', models.FloatField()),
                ('validity_in_days', models.IntegerField()),
                ('no_of_duties', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('tax', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.tax', to_field='tax_name')),
            ],
            options={
                'verbose_name_plural': 'Subscription',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.city', to_field='city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.country')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.state', to_field='state')),
            ],
            options={
                'verbose_name_plural': 'Location',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.country'),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.state', to_field='state'),
        ),
        migrations.AddField(
            model_name='branch',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.city', to_field='city'),
        ),
        migrations.AddField(
            model_name='branch',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.country'),
        ),
        migrations.AddField(
            model_name='branch',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.state', to_field='state'),
        ),
        migrations.AddField(
            model_name='branch',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.zone', to_field='zone_name'),
        ),
    ]
