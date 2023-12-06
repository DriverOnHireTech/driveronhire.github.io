# Generated by Django 4.2.1 on 2023-12-06 07:52

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_master', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_upload', models.ImageField(blank=True, default=None, null=True, upload_to='media')),
                ('first_name', models.CharField(default=None, max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('alt_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, default='info@driveronhire.com', max_length=254, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('Married', 'Married'), ('Single', 'Single')], max_length=10, null=True)),
                ('religion', models.CharField(blank=True, choices=[('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh')], max_length=10, null=True)),
                ('cast', models.CharField(blank=True, choices=[('Marathi', 'Marathi'), ('Muslim', 'Muslim'), ('Gujrati', 'Gujarati'), ('SO', 'SouthIndian'), ('Punjabi', 'Punjabi'), ('UP', 'UP'), ('Bihari', 'Bihari'), ('Other', 'Other')], default='MA', max_length=20, null=True)),
                ('region', models.CharField(blank=True, max_length=200, null=True)),
                ('qualification', models.CharField(blank=True, choices=[('5', '5th'), ('6', '6th'), ('7', '7th'), ('8', '8th'), ('9', '9th'), ('SSC', 'SSC'), ('HSC', 'HSC'), ('BC', 'BCOM'), ('BS', 'BSc'), ('BE', 'BE'), ('BA', 'BA')], default='SS', max_length=10, null=True)),
                ('driver_type', models.CharField(blank=True, choices=[('Part Time', 'Part Time'), ('Full Time', 'Full Time')], max_length=10, null=True)),
                ('language', models.CharField(blank=True, choices=[('Hindi', 'Hindi'), ('English', 'English'), ('Bhojpuri', 'Bhojpuri')], default='Hindi', max_length=100, null=True)),
                ('t_address', models.CharField(blank=True, max_length=200, null=True)),
                ('p_address', models.CharField(blank=True, max_length=200, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('aggrement_expiry_date', models.DateField(blank=True, null=True)),
                ('licence_no', models.CharField(blank=True, max_length=100, null=True)),
                ('licence_issued_from', models.CharField(blank=True, max_length=100, null=True)),
                ('licence_type', models.CharField(blank=True, choices=[('LMV-TR', 'LMV-TR'), ('LMV-NT', 'LMV-NT')], default='TR', max_length=10, null=True)),
                ('date_of_issue', models.DateField(blank=True, null=True)),
                ('date_of_expiry', models.DateField(blank=True, null=True)),
                ('present_salary', models.FloatField(blank=True, null=True)),
                ('expected_salary', models.FloatField(blank=True, null=True)),
                ('pan_card_no', models.CharField(blank=True, max_length=100, null=True)),
                ('aadhar_card_no', models.CharField(max_length=100)),
                ('blood_group', models.CharField(blank=True, choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=10, null=True)),
                ('passport', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('passport_no', models.CharField(blank=True, max_length=100, null=True)),
                ('heavy_vehicle', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('car_transmission', models.CharField(blank=True, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Luxury', 'Luxury')], max_length=10, null=True)),
                ('start_doh_date', models.DateField(blank=True, null=True)),
                ('car_company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('transmission_type', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Luxury', 'Luxury')], max_length=500, null=True)),
                ('car_type', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('SUV', 'SUV'), ('Sedan', 'Sedan'), ('Luxury', 'Luxury'), ('Hatchback', 'Hatchback'), ('MPV', 'MPV'), ('MUV', 'MUV'), ('Sedan Luxury', 'Sedan Luxury'), ('SUV Luxury', 'SUV Luxury')], max_length=500, null=True)),
                ('driven_km', models.FloatField(blank=True, null=True)),
                ('driving_licence', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('ration_card', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('pan_card', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('light_bill', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('aadhar_card', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('home_agreement', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('affidavit', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('pcc_certificate', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('company_name', models.CharField(blank=True, max_length=30, null=True)),
                ('address_location', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=20, null=True)),
                ('worked_from', models.DateField(blank=True, null=True)),
                ('worked_till', models.DateField(blank=True, null=True)),
                ('monthly_salary', models.FloatField(blank=True, null=True)),
                ('reason_for_leaving', models.CharField(blank=True, max_length=30, null=True)),
                ('car_driven', models.CharField(blank=True, max_length=20, null=True)),
                ('relationship', models.CharField(blank=True, max_length=100, null=True)),
                ('member_name', models.CharField(blank=True, max_length=100, null=True)),
                ('approx_age', models.IntegerField(blank=True, null=True)),
                ('mobile_no', models.CharField(blank=True, max_length=20, null=True)),
                ('education_details', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('reference', models.CharField(blank=True, max_length=15, null=True)),
                ('schedule_training', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('training_date', models.DateField(blank=True, null=True)),
                ('training_status', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('Purchase_uniform', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('scheduled_driving_test', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('driving_test_date', models.DateField(blank=True, null=True)),
                ('driving_status', models.CharField(blank=True, choices=[('Approve', 'Approve'), ('Reject', 'Reject')], max_length=10, null=True)),
                ('is_approval_done', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('police_verification', models.CharField(blank=True, choices=[('Processing', 'Processing'), ('Certified', 'Certified'), ('Rejected', 'Rejected')], max_length=10, null=True)),
                ('week_off', models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10, null=True)),
                ('scheme_type', models.CharField(blank=True, choices=[('Platinum', 'Platinum'), ('Gold', 'Gold'), ('Silver', 'Silver'), ('Diwali', 'Diwali'), ('Gold2', 'Gold2'), ('Platinum2', 'Platinum2')], max_length=10, null=True)),
                ('driver_status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Suspended', 'Suspended')], max_length=10, null=True)),
                ('driver_rating', models.PositiveBigIntegerField(blank=True, null=True)),
                ('driverlocation', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, help_text='Point(latitude longitude)', null=True, srid=4326, verbose_name='Location in Map')),
                ('total_exp', models.IntegerField(blank=True, null=True)),
                ('driver_update_date', models.DateField(auto_now_add=True, null=True)),
                ('has_received_notification', models.BooleanField(blank=True, default=False, null=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.branch')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.city')),
                ('driver_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.location')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.state')),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.zone')),
            ],
        ),
        migrations.CreateModel(
            name='BasicDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_upload', models.ImageField(default=None, upload_to='media')),
                ('first_name', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(blank=True, default='Male', max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('alt_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=20, null=True)),
                ('religion', models.CharField(blank=True, max_length=30, null=True)),
                ('qualification', models.CharField(blank=True, default='SS', max_length=20, null=True)),
                ('language', models.CharField(blank=True, default='Hindi', max_length=100, null=True)),
                ('temp_address', models.CharField(blank=True, max_length=200, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('aggrement_expiry_date', models.DateField(blank=True, null=True)),
                ('licence_no', models.CharField(blank=True, max_length=20, null=True)),
                ('licence_issued_from', models.CharField(blank=True, max_length=20, null=True)),
                ('licence_type', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_issue', models.DateField(blank=True, null=True)),
                ('date_of_expiry', models.DateField(blank=True, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.city')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.state')),
            ],
        ),
        migrations.CreateModel(
            name='DriverBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RmVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcc_certificate', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('driver_type', models.CharField(max_length=15)),
                ('region', models.CharField(max_length=30)),
                ('car_transmission', models.CharField(max_length=20)),
                ('schedule_training', models.CharField(max_length=10)),
                ('training_date', models.DateField()),
                ('training_status', models.CharField(max_length=10)),
                ('Purchase_uniform', models.CharField(max_length=10)),
                ('scheduled_driving_test', models.CharField(max_length=10)),
                ('driving_test_date', models.DateField()),
                ('driving_status', models.CharField(max_length=10)),
                ('is_approval_done', models.CharField(max_length=10)),
                ('police_verification', models.CharField(max_length=10)),
                ('week_off', models.CharField(max_length=10)),
                ('scheme_type', models.CharField(max_length=10)),
                ('driver_status', models.CharField(max_length=10)),
                ('driver_rating', models.PositiveBigIntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.branch')),
                ('driver_number', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='driver_management.basicdetail')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.zone')),
            ],
        ),
        migrations.CreateModel(
            name='ReferDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.PositiveBigIntegerField()),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.branch')),
                ('referdrivername', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driverlocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driverlocation', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, help_text='Point(longitude latitude)', null=True, srid=4326, verbose_name='Location in Map')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driverleave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('leave_from_date', models.DateField()),
                ('leave_to_date', models.DateField()),
                ('total_days_of_leave', models.IntegerField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('driver_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driverappstatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.CharField(blank=True, choices=[('Gold', 'Gold'), ('Gold2', 'Gold2'), ('Platinium', 'Platinium'), ('Platinium2', 'Platinium2'), ('silver', 'silver'), ('DiwaliScheme', 'DiwaliScheme')], max_length=100, null=True)),
                ('paymentamount', models.BigIntegerField(blank=True, null=True)),
                ('is_paid', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(blank=True, choices=[('active', 'active'), ('inactive', 'inactive')], max_length=100, null=True)),
                ('drivername', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='driver_management.adddriver')),
            ],
        ),
        migrations.CreateModel(
            name='BgVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pan_card_no', models.CharField(blank=True, max_length=15, null=True)),
                ('aadhar_card_no', models.CharField(max_length=20)),
                ('blood_group', models.CharField(max_length=10)),
                ('passport', models.CharField(blank=True, max_length=10, null=True)),
                ('passport_no', models.CharField(blank=True, max_length=20, null=True)),
                ('heavy_vehicle', models.CharField(blank=True, max_length=10, null=True)),
                ('car_transmission', models.CharField(max_length=10)),
                ('start_doh_date', models.DateField()),
                ('car_company_name', models.CharField(blank=True, max_length=15, null=True)),
                ('transmission_type', models.CharField(max_length=10)),
                ('car_type', models.CharField(max_length=10)),
                ('driven_km', models.FloatField()),
                ('driving_licence', models.FileField(default=None, upload_to='documents/%Y/%m/')),
                ('ration_card', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('pan_card', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('light_bill', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('aadhar_card', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('home_agreement', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('affidavit', models.FileField(blank=True, default=None, null=True, upload_to='documents/%Y/%m/')),
                ('company_name', models.CharField(max_length=30)),
                ('address_location', models.CharField(max_length=100)),
                ('contact_person', models.CharField(max_length=20)),
                ('worked_from', models.DateField()),
                ('worked_till', models.DateField()),
                ('monthly_salary', models.FloatField()),
                ('reason_for_leaving', models.CharField(max_length=30)),
                ('car_driven', models.CharField(max_length=20)),
                ('relationship', models.CharField(max_length=100)),
                ('member_name', models.CharField(max_length=100)),
                ('approx_age', models.IntegerField()),
                ('mobile_no', models.CharField(max_length=20)),
                ('education_details', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('reference', models.CharField(max_length=15)),
                ('driver_number', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='driver_management.basicdetail')),
            ],
        ),
    ]
