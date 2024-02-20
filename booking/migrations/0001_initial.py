# Generated by Django 4.2.1 on 2024-02-19 11:37

import datetime
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
            name='AgentBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile_number', models.BigIntegerField(blank=True, null=True)),
                ('Alternet_number', models.BigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('client_location', django.contrib.gis.db.models.fields.PointField(blank=True, default='POINT (0 0)', null=True, srid=4326)),
                ('car_company', models.CharField(blank=True, max_length=100, null=True)),
                ('car_type', models.CharField(blank=True, max_length=100, null=True)),
                ('car_transmission', models.CharField(blank=True, max_length=100, null=True)),
                ('bookingfor', models.CharField(blank=True, choices=[('local', 'local'), ('drop', 'drop'), ('outstation', 'outstation')], max_length=150, null=True)),
                ('source', models.CharField(blank=True, max_length=100, null=True)),
                ('bookingfordate', models.DateTimeField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('request_type', models.CharField(blank=True, max_length=200, null=True)),
                ('trip_type', models.CharField(blank=True, max_length=200, null=True)),
                ('packege', models.CharField(blank=True, max_length=100, null=True)),
                ('visiting_location', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(blank=True, choices=[('pending', 'pending'), ('active', 'active'), ('completed', 'completed'), ('cancelled', 'cancelled')], max_length=100, null=True)),
                ('cancelbooking_reason', models.CharField(blank=True, choices=[('Not in Uniform', 'Not in Uniform'), ('Plan got cancel', 'Plan got cancel'), ('Driver was not looking good', 'Driver was not looking good'), ('Asking advance money', 'Asking advance money'), ('Driver was smelling', 'Driver was smelling'), ('Isolation cover not there', 'Isolation cover not there'), ('Not reach on time', 'Not reach on time'), ('Driver not received my call', 'Driver not received my call'), ('Booked by mistake', 'Booked by mistake'), ('Charges issue', 'Charges issue')], max_length=500, null=True)),
                ('booking_created_by_name', models.CharField(blank=True, max_length=255, null=True)),
                ('deuty_started', models.TimeField(blank=True, null=True)),
                ('journy_started', models.CharField(choices=[('journy started', 'journy started'), ('journy end', 'journy end')], default='pending', max_length=100)),
                ('deuty_end', models.DateTimeField(blank=True, null=True)),
                ('guest_booking', models.BooleanField(default=False)),
                ('bookingdt', models.DateField(auto_now_add=True, null=True)),
                ('booking_time', models.TimeField(auto_now_add=True, null=True)),
                ('accepted_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_driver_id', to=settings.AUTH_USER_MODEL)),
                ('booking_created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agentbookings_created_by', to=settings.AUTH_USER_MODEL)),
                ('driver_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agentbookings_driver_name', to='driver_management.adddriver')),
            ],
        ),
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
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('z_name', models.CharField(max_length=100, unique=True)),
                ('extra_charge', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='userProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.PositiveBigIntegerField(blank=True, null=True)),
                ('user_address', models.CharField(blank=True, max_length=200, null=True)),
                ('user_car', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('trip_type', models.CharField(blank=True, max_length=50, null=True)),
                ('booking_type', models.CharField(blank=True, max_length=50, null=True)),
                ('packege', models.CharField(blank=True, max_length=100, null=True)),
                ('booking_date', models.DateField(blank=True, null=True)),
                ('client_booking_time', models.TimeField(blank=True, default=datetime.time(12, 0), null=True)),
                ('no_of_days', models.PositiveIntegerField(blank=True, null=True)),
                ('currant_location', django.contrib.gis.db.models.fields.PointField(blank=True, default='POINT (0 0)', null=True, srid=4326)),
                ('user_address', models.CharField(blank=True, max_length=500, null=True)),
                ('car_type', models.CharField(max_length=100, null=True)),
                ('gear_type', models.CharField(max_length=100, null=True)),
                ('pickup_location', models.CharField(blank=True, max_length=500, null=True)),
                ('drop_location', models.CharField(blank=True, max_length=500, null=True)),
                ('Charges', models.BigIntegerField(blank=True, null=True)),
                ('outskirt_charge', models.BigIntegerField(blank=True, default=0, null=True)),
                ('notification_sent', models.BooleanField(blank=True, default=False, null=True)),
                ('status', models.CharField(choices=[('accept', 'accept'), ('decline', 'decline'), ('pending', 'pending'), ('completed', 'completed'), ('cancelled', 'cancelled')], default='pending', max_length=100)),
                ('cancelbooking_reason', models.CharField(blank=True, max_length=500, null=True)),
                ('cancelbooking_message', models.CharField(blank=True, max_length=1000, null=True)),
                ('accepted_driver_name', models.CharField(blank=True, max_length=255, null=True)),
                ('accepted_driver_number', models.CharField(blank=True, max_length=255, null=True)),
                ('deuty_started', models.DateTimeField(blank=True, null=True)),
                ('deuty_end', models.DateTimeField(blank=True, null=True)),
                ('journy_started', models.CharField(choices=[('journy started', 'journy started'), ('journy end', 'journy end')], default='pending', max_length=100)),
                ('booking_time', models.DateTimeField(auto_now_add=True)),
                ('accepted_driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_driver', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='driver_name', to='driver_management.adddriver')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotifydriversAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateField(auto_now=True)),
                ('agent_booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.agentbooking')),
                ('driver', models.ManyToManyField(to='driver_management.adddriver')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifydrivers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateField(auto_now=True)),
                ('driver', models.ManyToManyField(to='driver_management.adddriver')),
                ('place_booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.placebooking')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_favourite', models.BooleanField(blank=True, default=False, null=True)),
                ('base_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('night_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('outskirt_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('extra_hour_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('additional_hours', models.IntegerField(blank=True, default=0, null=True)),
                ('total_charge', models.IntegerField(blank=True, default=0, null=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='driver_management.adddriver')),
                ('placebooking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.placebooking')),
            ],
        ),
        migrations.CreateModel(
            name='GuestBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_for', models.CharField(blank=True, choices=[('Local', 'Local'), ('outstation', 'outstation')], max_length=50, null=True)),
                ('trip_type', models.CharField(blank=True, choices=[('OneWay', 'OneWay'), ('Round Trip', 'Round Trip')], max_length=50, null=True)),
                ('required_driver', models.DateTimeField(blank=True, null=True)),
                ('client_phone', models.PositiveBigIntegerField(blank=True, null=True)),
                ('request_date', models.DateTimeField(blank=True, null=True)),
                ('request_time', models.TimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
        migrations.CreateModel(
            name='Declinebooking1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('refuse_time', models.DateField(auto_now_add=True)),
                ('agentbooking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.agentbooking')),
                ('placebooking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.placebooking')),
                ('refuse_driver_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Declinebooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('refuse_time', models.DateField(auto_now_add=True)),
                ('agentbooking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.agentbooking')),
                ('placebooking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.placebooking')),
                ('refuse_driver_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookLater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.PositiveBigIntegerField(blank=True, null=True)),
                ('trip_type', models.CharField(blank=True, max_length=50, null=True)),
                ('packege', models.CharField(blank=True, max_length=100, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('currant_location', django.contrib.gis.db.models.fields.PointField(blank=True, default='POINT (0 0)', null=True, srid=4326)),
                ('car_type', models.CharField(max_length=100, null=True)),
                ('gear_type', models.CharField(max_length=100, null=True)),
                ('pickup_location', models.CharField(max_length=100, null=True)),
                ('drop_location', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('accept', 'accept'), ('decline', 'decline'), ('pending', 'pending'), ('completed', 'completed')], default='pending', max_length=20)),
                ('schedule_booking', models.DateTimeField(blank=True, null=True)),
                ('booking_time', models.DateTimeField(auto_now_add=True)),
                ('accepted_driver', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='driver_name', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AddfavoriteDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_favorite', models.BooleanField(default=False)),
                ('driver_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
