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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile= models.PositiveBigIntegerField()
    trip_type=models.CharField(max_length=50, null=True ,blank=True)
    packege= models.CharField(max_length=100, null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    currant_location = gis_point.PointField(default='POINT (0 0)',srid=4326, blank=True, null=True)
    car_type=models.CharField(max_length=100, null=True)
    gear_type= models.CharField(max_length=100, null=True)
    pickup_location=models.CharField(max_length=100, null=True)
    drop_location=models.CharField(max_length=100, null=True)
    status =  models.CharField(max_length=20, choices=STATUS, default='pending')
    accepted_driver =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_driver', null=True, blank=True)
    booking_time=models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.trip_type
    

class Invoice(models.Model):
    user =  models.ForeignKey(bookinguser, on_delete=models.CASCADE)
    driver = models.ForeignKey(AddDriver, on_delete=models.CASCADE)
    placebooking = models.ForeignKey(PlaceBooking, on_delete=models.CASCADE)
    add_favourite = models.BooleanField(default=False)
    invoice_generate =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name
  

class Feedback(models.Model):
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating =  models.IntegerField()
    descriptions = models.CharField(max_length=300, null=True, blank=True)
    ratingdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
    

"""This model for user Profile"""
class Profile(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    userlocation= gis_point.PointField(
        "Location in Map", geography=True, blank=True, null=True,
        srid=4326, help_text="Point(longitude latitude)")
    
    def __str__(self):
        return str(self.user.phone)
    


class AddfavoriteDriver(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='Customer')
    driver_name= models.ForeignKey(User, on_delete=models.CASCADE)
    add_favorite=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.phone)


class AgentBooking(models.Model):
    booking_type= (
        ('local', 'local'),
        ('drop', 'drop'),
        ('outstation', 'outstation')
    )
    client_name= models.CharField(max_length=200, null=True, blank=True)
    mobile_number= models.BigIntegerField(null=True, blank=True)
    Alternet_number= models.BigIntegerField(null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    Address=models.CharField(max_length=500, null=True, blank=True)
    car= models.CharField(max_length=100, null=True, blank=True)
    bookingfor= models.CharField(choices=booking_type, null=True, blank=True)
    source= models.CharField(max_length=100, null=True,blank=True)
    from_date= models.DateField(auto_now_add=False, null=True, blank=True)
    to_date=models.DateField(auto_now_add=False,null=True, blank=True)
    start_time=models.TimeField(auto_now_add=False, null=True, blank=True)
    religion= models.CharField(max_length=100, null=True,blank=True)
    request_type=models.CharField(max_length=100, null=True, blank=True)
    trip_type=models.CharField(max_length=100, null=True, blank=True)
    packege=  models.CharField(max_length=100, null=True, blank=True)
    bookingdt= models.DateField(auto_now_add=True)

    def __str__(self):
        return self.client_name


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
    from_date = models.DateField(null=True, blank=True)
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