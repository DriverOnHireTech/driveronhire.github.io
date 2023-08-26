from django.db import models
from datetime import datetime
from django.conf import settings
# from django.contrib.auth.models import User
# from authentication.models import User
from driver_management.models import AddDriver


class Enquiry(models.Model):
    booking_type = models.CharField(choices=(("1", "Local"), ("2", "Outstation"), ("3", "Drop")),
                                    max_length=10)
    date_of_enquiry = models.DateTimeField(default=datetime.now)
    client_name = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=15)
    alternate_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=20)
    duty_hours = models.CharField(choices=(("1", "4 Hours"), ("2", "8 Hours"), ("3", "12 Hours")),
                                  max_length=10)
    car_details = models.CharField(max_length=20)
    created_by = models.ForeignKey(AddDriver, on_delete=models.CASCADE)

    def __str__(self):
        return self.client_name

