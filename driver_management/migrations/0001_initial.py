<<<<<<< HEAD
# Generated by Django 4.2.1 on 2023-07-31 11:53
=======
# Generated by Django 4.2.1 on 2023-07-27 12:25
>>>>>>> 3b863214f796e66470316d24c4829e269910068f

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        ('user_master', '0001_initial'),
=======
        ("user_master", "0001_initial"),
>>>>>>> 3b863214f796e66470316d24c4829e269910068f
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DriverHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            ],
        ),
        migrations.CreateModel(
            name='ReferDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ViewDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Driverlocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_lat', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('driver_long', models.DecimalField(blank=True, decimal_places=6, max_digits=10, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AddDriver',
            fields=[
<<<<<<< HEAD
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_upload', models.ImageField(default=None, upload_to='images/%Y/%m/')),
                ('first_name', models.CharField(default=None, max_length=20)),
                ('middle_name', models.CharField(blank=True, max_length=20, null=True)),
                ('last_name', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10)),
                ('date_of_birth', models.DateField()),
                ('mobile', models.CharField(max_length=15)),
                ('alt_mobile', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('marital_status', models.CharField(choices=[('Married', 'Married'), ('Single', 'Single')], max_length=10)),
                ('religion', models.CharField(choices=[('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Christian', 'Christian'), ('Sikh', 'Sikh')], max_length=10)),
                ('cast', models.CharField(choices=[('Marathi', 'Marathi'), ('Muslim', 'Muslim'), ('Gujrati', 'Gujarati'), ('SO', 'SouthIndian'), ('Punjabi', 'Punjabi'), ('UP', 'UP'), ('Bihari', 'Bihari'), ('Other', 'Other')], default='MA', max_length=20)),
                ('qualification', models.CharField(choices=[('5', '5th'), ('6', '6th'), ('7', '7th'), ('8', '8th'), ('9', '9th'), ('SSC', 'SSC'), ('HSC', 'HSC'), ('BC', 'BCOM'), ('BS', 'BSc'), ('BE', 'BE'), ('BA', 'BA')], default='SS', max_length=10)),
                ('driver_type', models.CharField(choices=[('Temporary', 'Temporary'), ('Permanent', 'Permanent')], default='Temporary', max_length=10)),
                ('language', models.CharField(choices=[('Hindi', 'Hindi'), ('English', 'English'), ('Bhojpuri', 'Bhojpuri')], default='Hindi', max_length=10)),
                ('t_address', models.CharField(max_length=200)),
                ('p_address', models.CharField(max_length=200)),
                ('pincode', models.CharField(blank=True, max_length=10, null=True)),
                ('aggrement_expiry_date', models.DateField()),
                ('licence_no', models.CharField(max_length=20)),
                ('licence_issued_from', models.CharField(max_length=20)),
                ('licence_type', models.CharField(choices=[('LMV-TR', 'LMV-TR'), ('LMV-NT', 'LMV-NT')], default='TR', max_length=10)),
                ('date_of_issue', models.DateField()),
                ('date_of_expiry', models.DateField()),
                ('present_salary', models.FloatField(blank=True, null=True)),
                ('expected_salary', models.FloatField()),
                ('pan_card_no', models.CharField(blank=True, max_length=15, null=True)),
                ('aadhar_card_no', models.CharField(max_length=20)),
                ('blood_group', models.CharField(choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=10)),
                ('passport', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('passport_no', models.CharField(blank=True, max_length=20, null=True)),
                ('heavy_vehicle', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True)),
                ('car_transmission', models.CharField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Luxury', 'Luxury')], max_length=10)),
                ('start_doh_date', models.DateField()),
                ('end_doh_date', models.DateField()),
                ('car_company_name', models.CharField(blank=True, max_length=15, null=True)),
                ('transmission_type', models.CharField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic'), ('Luxury', 'Luxury')], max_length=10)),
                ('car_type', models.CharField(choices=[('SUV', 'SUV'), ('Sedan', 'Sedan'), ('Luxury', 'Luxury'), ('Hatchback', 'Hatchback'), ('MPV', 'MPV'), ('MUV', 'MUV')], max_length=10)),
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
                ('relationship', models.CharField(max_length=20)),
                ('member_name', models.CharField(max_length=20)),
                ('approx_age', models.IntegerField()),
                ('mobile_no', models.CharField(max_length=20)),
                ('education_details', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('reference', models.CharField(max_length=15)),
                ('schedule_training', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('training_date', models.DateField()),
                ('training_status', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('Purchase_uniform', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('scheduled_driving_test', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('driving_test_date', models.DateField()),
                ('driving_status', models.CharField(choices=[('Approve', 'Approve'), ('Reject', 'Reject')], max_length=10)),
                ('is_approval_done', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('police_verification', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10)),
                ('week_off', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10)),
                ('scheme_type', models.CharField(choices=[('Platinum', 'Platinum'), ('Gold', 'Gold'), ('Silver', 'Silver')], max_length=10)),
                ('driver_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Suspended', 'Suspended')], max_length=10)),
                ('driver_rating', models.PositiveBigIntegerField()),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.branch')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.city')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.location')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_master.state')),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_master.zone')),
=======
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image_upload",
                    models.ImageField(default=None, upload_to="images/%Y/%m/"),
                ),
                ("first_name", models.CharField(default=None, max_length=20)),
                ("middle_name", models.CharField(blank=True, max_length=20, null=True)),
                ("last_name", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "sex",
                    models.CharField(
                        choices=[("Male", "Male"), ("Female", "Female")],
                        default="Male",
                        max_length=10,
                    ),
                ),
                ("date_of_birth", models.DateField()),
                ("mobile", models.CharField(max_length=15)),
                ("alt_mobile", models.CharField(blank=True, max_length=15, null=True)),
                ("email", models.EmailField(max_length=254)),
                (
                    "marital_status",
                    models.CharField(
                        choices=[("Married", "Married"), ("Single", "Single")],
                        max_length=10,
                    ),
                ),
                (
                    "religion",
                    models.CharField(
                        choices=[
                            ("Hindu", "Hindu"),
                            ("Muslim", "Muslim"),
                            ("Christian", "Christian"),
                            ("Sikh", "Sikh"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "cast",
                    models.CharField(
                        choices=[
                            ("Marathi", "Marathi"),
                            ("Muslim", "Muslim"),
                            ("Gujrati", "Gujarati"),
                            ("SO", "SouthIndian"),
                            ("Punjabi", "Punjabi"),
                            ("UP", "UP"),
                            ("Bihari", "Bihari"),
                            ("Other", "Other"),
                        ],
                        default="MA",
                        max_length=20,
                    ),
                ),
                (
                    "qualification",
                    models.CharField(
                        choices=[
                            ("5", "5th"),
                            ("6", "6th"),
                            ("7", "7th"),
                            ("8", "8th"),
                            ("9", "9th"),
                            ("SSC", "SSC"),
                            ("HSC", "HSC"),
                            ("BC", "BCOM"),
                            ("BS", "BSc"),
                            ("BE", "BE"),
                            ("BA", "BA"),
                        ],
                        default="SS",
                        max_length=10,
                    ),
                ),
                (
                    "driver_type",
                    models.CharField(
                        choices=[
                            ("Temporary", "Temporary"),
                            ("Permanent", "Permanent"),
                        ],
                        default="Temporary",
                        max_length=10,
                    ),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("Hindi", "Hindi"),
                            ("English", "English"),
                            ("Bhojpuri", "Bhojpuri"),
                        ],
                        default="Hindi",
                        max_length=10,
                    ),
                ),
                ("t_address", models.CharField(max_length=200)),
                ("p_address", models.CharField(max_length=200)),
                ("pincode", models.CharField(max_length=10)),
                ("aggrement_expiry_date", models.DateField()),
                ("licence_no", models.CharField(max_length=20)),
                ("licence_issued_from", models.CharField(max_length=20)),
                (
                    "licence_type",
                    models.CharField(
                        choices=[("LMV-TR", "LMV-TR"), ("LMV-NT", "LMV-NT")],
                        default="TR",
                        max_length=10,
                    ),
                ),
                ("date_of_issue", models.DateField()),
                ("date_of_expiry", models.DateField()),
                ("present_salary", models.FloatField(blank=True, null=True)),
                ("expected_salary", models.FloatField()),
                ("pan_card_no", models.CharField(blank=True, max_length=15, null=True)),
                ("aadhar_card_no", models.CharField(max_length=20)),
                (
                    "blood_group",
                    models.CharField(
                        choices=[
                            ("O+", "O+"),
                            ("O-", "O-"),
                            ("A+", "A+"),
                            ("A-", "A-"),
                            ("B+", "B+"),
                            ("B-", "B-"),
                            ("AB+", "AB+"),
                            ("AB-", "AB-"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "passport",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                ("passport_no", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "heavy_vehicle",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                (
                    "car_transmission",
                    models.CharField(
                        choices=[
                            ("Manual", "Manual"),
                            ("Automatic", "Automatic"),
                            ("Luxury", "Luxury"),
                        ],
                        max_length=10,
                    ),
                ),
                ("start_doh_date", models.DateField()),
                ("end_doh_date", models.DateField()),
                ("car_company_name", models.CharField(max_length=15)),
                (
                    "transmission_type",
                    models.CharField(
                        choices=[
                            ("Manual", "Manual"),
                            ("Automatic", "Automatic"),
                            ("Luxury", "Luxury"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "car_type",
                    models.CharField(
                        choices=[
                            ("SUV", "SUV"),
                            ("Sedan", "Sedan"),
                            ("Luxury", "Luxury"),
                            ("Hatchback", "Hatchback"),
                            ("MPV", "MPV"),
                            ("MUV", "MUV"),
                        ],
                        max_length=10,
                    ),
                ),
                ("driven_km", models.FloatField()),
                (
                    "driving_licence",
                    models.FileField(default=None, upload_to="documents/%Y/%m/"),
                ),
                (
                    "ration_card",
                    models.FileField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="documents/%Y/%m/",
                    ),
                ),
                (
                    "pan_card",
                    models.FileField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="documents/%Y/%m/",
                    ),
                ),
                (
                    "light_bill",
                    models.FileField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="documents/%Y/%m/",
                    ),
                ),
                (
                    "aadhar_card",
                    models.FileField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="documents/%Y/%m/",
                    ),
                ),
                (
                    "home_agreement",
                    models.FileField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="documents/%Y/%m/",
                    ),
                ),
                (
                    "affidavit",
                    models.FileField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="documents/%Y/%m/",
                    ),
                ),
                ("company_name", models.CharField(max_length=30)),
                ("address_location", models.CharField(max_length=100)),
                ("contact_person", models.CharField(max_length=20)),
                ("worked_from", models.DateField()),
                ("worked_till", models.DateField()),
                ("monthly_salary", models.FloatField()),
                ("reason_for_leaving", models.CharField(max_length=30)),
                ("car_driven", models.CharField(max_length=20)),
                ("relationship", models.CharField(max_length=20)),
                ("member_name", models.CharField(max_length=20)),
                ("approx_age", models.IntegerField()),
                ("mobile_no", models.CharField(max_length=20)),
                ("education_details", models.CharField(max_length=20)),
                ("address", models.CharField(max_length=200)),
                ("reference", models.CharField(max_length=15)),
                (
                    "schedule_training",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                ("training_date", models.DateField()),
                (
                    "training_status",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                (
                    "Purchase_uniform",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                (
                    "scheduled_driving_test",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                ("driving_test_date", models.DateField()),
                (
                    "driving_status",
                    models.CharField(
                        choices=[("Approve", "Approve"), ("Reject", "Reject")],
                        max_length=10,
                    ),
                ),
                (
                    "is_approval_done",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                (
                    "police_verification",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")], max_length=10
                    ),
                ),
                (
                    "week_off",
                    models.CharField(
                        choices=[
                            ("Monday", "Monday"),
                            ("Tuesday", "Tuesday"),
                            ("Wednesday", "Wednesday"),
                            ("Thursday", "Thursday"),
                            ("Friday", "Friday"),
                            ("Saturday", "Saturday"),
                            ("Sunday", "Sunday"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "scheme_type",
                    models.CharField(
                        choices=[
                            ("Platinum", "Platinum"),
                            ("Gold", "Gold"),
                            ("Silver", "Silver"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "driver_status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Approved", "Approved"),
                            ("Rejected", "Rejected"),
                            ("Suspended", "Suspended"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_master.branch",
                    ),
                ),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_master.city",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_master.location",
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_master.state",
                    ),
                ),
                (
                    "zone",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user_master.zone",
                    ),
                ),
>>>>>>> 3b863214f796e66470316d24c4829e269910068f
            ],
        ),
    ]
