"""
This is booking models
"""
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.contrib.gis.db import models as gis_point
# from django.contrib.gis.geos import Point
from django.conf import settings
from authentication.models import User
# from client_management.models import AddClient
from driver_management.models import AddDriver
from datetime import time
from twilio.rest import Client
from geopy.geocoders import Nominatim



class bookinguser(models.Model):
    cities=(
        ('Mumbai', 'Mumbai'),
        ("Navi Mumbai", "Navi Mumbai"),
        ("Thane", "Thane"),
        ("Pune", "Pune"),
        ("Bangaluru", "Bangaluru"),
        ("Delhi", "Delhi")
    )
    full_name=models.CharField(max_length=200, null=True, blank=True)
    mobile_number=models.CharField(max_length=14)
    city=models.CharField(choices=cities,max_length=100, null=True, blank=True, default="Mumbai")
    address= models.CharField(max_length=200, null=True, blank=True)
    


    def __str__(self):
        return self.full_name


class PlaceBooking(models.Model):
    STATUS=(
        ('accept','accept'),
        ('decline', 'decline'),
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled')
    )
    reason=(
        ("Not in Uniform", "Not in Uniform"),
        ("Plan got cancel", "Plan got cancel"),
        ("Driver was not looking good","Driver was not looking good"),
        ("Asking advance money", "Asking advance money"),
        ("Driver was smelling", "Driver was smelling"),
        ("Isolation cover not there", "Isolation cover not there"),
        ("Not reach on time", "Not reach on time"),
        ("Driver not received my call", "Driver not received my call"),
        ("Booked by mistake", "Booked by mistake"),
        ("Charges issue", "Charges issue")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    mobile= models.PositiveBigIntegerField(null=True, blank=True)
    trip_type=models.CharField(max_length=50, null=True ,blank=True)
    packege= models.CharField(max_length=100, null=True, blank=True)
    booking_date= models.DateField(auto_now_add=False, null=True, blank=True)
    client_booking_time = models.TimeField(default=time(12,0), null=True, blank=True)
    no_of_days= models.PositiveIntegerField(null=True, blank=True)
    currant_location = gis_point.PointField(default='POINT (0 0)',srid=4326, blank=True, null=True)
    user_address=models.CharField(max_length=500, null=True, blank=True)
    car_type=models.CharField(max_length=100, null=True)
    gear_type= models.CharField(max_length=100, null=True)
    pickup_location=models.CharField(max_length=500, null=True, blank=True)
    drop_location=models.CharField(max_length=100, null=True, blank=True)
    notification_sent = models.BooleanField(default=False, null=True, blank=True)
    status =  models.CharField(max_length=100, choices=STATUS, default='pending')
    cancelbooking_reason=models.CharField(max_length=500, null=True, blank=True)
    cancelbooking_message = models.CharField(max_length=1000, null=True, blank=True)
    accepted_driver =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accepted_driver', null=True, blank=True)
    deuty_started=models.DateTimeField(auto_now_add=True)
    booking_time=models.DateTimeField(auto_now_add=True)
    
   
    def __str__(self):
        return f"{self.id}"
    
    """Save method"""
    #Write here
    def save(self, *args, **kwargs):
        if self.currant_location:
            geolocator = Nominatim(user_agent="booking")
            location = geolocator.geocode(self.currant_location)

            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude

        super().save(*args, **kwargs)
    """"end save method"""

"""Agent booking"""
class AgentBooking(models.Model):
    booking_type= (
        ('local', 'local'),
        ('drop', 'drop'),
        ('outstation', 'outstation')
    )
    reason=(
        ("Not in Uniform", "Not in Uniform"),
        ("Plan got cancel", "Plan got cancel"),
        ("Driver was not looking good","Driver was not looking good"),
        ("Asking advance money", "Asking advance money"),
        ("Driver was smelling", "Driver was smelling"),
        ("Isolation cover not there", "Isolation cover not there"),
        ("Not reach on time", "Not reach on time"),
        ("Driver not received my call", "Driver not received my call"),
        ("Booked by mistake", "Booked by mistake"),
        ("Charges issue", "Charges issue")
    )
    Status=(('pending','pending'),('active', 'active'), ('completed', 'completed'))
    # id = models.AutoField(primary_key=True)
    client_name= models.CharField(max_length=200, null=True, blank=True)
    mobile_number= models.BigIntegerField(null=True, blank=True)
    Alternet_number= models.BigIntegerField(null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    address=models.CharField(max_length=500, null=True, blank=True)
    client_location = gis_point.PointField(default='POINT (0 0)',srid=4326, blank=True, null=True)
    car_company= models.CharField(max_length=100, null=True, blank=True)
    car_type = models.CharField(max_length=100, blank=True, null=True)
    car_transmission = models.CharField(max_length=100, blank=True, null=True)
    bookingfor= models.CharField(choices=booking_type,max_length=150, null=True, blank=True)
    source= models.CharField(max_length=100, null=True,blank=True)
    #from_date= models.DateField(auto_now_add=False, null=True, blank=True)
    to_date=models.DateField(auto_now_add=False,null=True, blank=True)
    start_time=models.TimeField(auto_now_add=False, null=True, blank=True)
    religion= models.CharField(max_length=100, null=True,blank=True)
    request_type=models.CharField(max_length=200, null=True, blank=True)
    trip_type=models.CharField(max_length=200, null=True, blank=True)
    packege=  models.CharField(max_length=100, null=True, blank=True)
    visiting_location= models.CharField(max_length=200, null=True, blank=True)
    status= models.CharField(choices=Status, max_length=100, null=True, blank=True)
    cancelbooking_reason=models.CharField(choices=reason,max_length=500, null=True, blank=True)
    driver_name= models.ForeignKey(AddDriver, on_delete=models.CASCADE, null=True, blank=True)
    booking_created_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    bookingdt= models.DateField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.client_name
    
"""End Agent booking"""
    
"""Save notifications"""
class Notifydrivers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    place_booking = models.ForeignKey(PlaceBooking, on_delete=models.CASCADE, null=True, blank=True)
    agent_booking=models.ForeignKey(AgentBooking, on_delete=models.CASCADE, null=True, blank=True)
    driver=models.ManyToManyField(AddDriver)
    received_at=models.DateField(auto_now=True)

    def __str__(self):
        return str(self.place_booking)
    
    # Testing purpose

"""End Notifications"""

class userProfile(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    mobile= models.PositiveBigIntegerField(null=True, blank=True)
    user_address= models.CharField(max_length=200, null=True, blank=True)
    user_car= models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user.phone)
    


class Invoice(models.Model):
    # user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    driver = models.ForeignKey(AddDriver, on_delete=models.CASCADE, null=True, blank=True)
    placebooking = models.ForeignKey(PlaceBooking, on_delete=models.CASCADE,null=True, blank=True)
    add_favourite = models.BooleanField(default=False, null=True, blank=True)
    invoice_generate =  models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.driver.first_name
  

class Feedback(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating =  models.IntegerField()
    descriptions = models.CharField(max_length=300, null=True, blank=True)
    ratingdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
    

"""This model for user Profile"""
    


class AddfavoriteDriver(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='Customer')
    driver_name= models.ForeignKey(User, on_delete=models.CASCADE)
    add_favorite=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.phone)


class BookLater(models.Model):
    STATUS=(
        ('accept','accept'),
        ('decline', 'decline'),
        ('pending', 'pending'),
        ('completed', 'completed')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile= models.PositiveBigIntegerField(null=True, blank=True)
    trip_type=models.CharField(max_length=50, null=True ,blank=True)
    packege= models.CharField(max_length=100, null=True, blank=True)
    #from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    currant_location = gis_point.PointField(default='POINT (0 0)',srid=4326, blank=True, null=True)
    car_type=models.CharField(max_length=100, null=True)
    gear_type= models.CharField(max_length=100, null=True)
    pickup_location=models.CharField(max_length=100, null=True)
    drop_location=models.CharField(max_length=100, null=True)
    status =  models.CharField(max_length=20, choices=STATUS, default='pending')
    accepted_driver =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_name', default=1)
    schedule_booking = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    booking_time=models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return self.trip_type
    
"""Geust Booking"""
class GuestBooking(models.Model):
    TRIP_FOR=(('Local','Local'),('outstation', 'outstation'))
    TRIP_TYPE=(('OneWay', "OneWay"), ("Round Trip", "Round Trip"))
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    trip_for=models.CharField(choices=TRIP_FOR,max_length=50, null=True ,blank=True)
    trip_type=models.CharField(choices=TRIP_TYPE,max_length=50, null=True ,blank=True)
    required_driver=models.DateTimeField(auto_now_add=False)
    client_phone= models.PositiveBigIntegerField(null=True, blank=True)
    request_date=models.DateTimeField(auto_now_add=False)
    request_time=models.TimeField(auto_now_add=False)

    def __str__(self):
        return self.trip_type

"""End"""