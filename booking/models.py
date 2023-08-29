from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models as gis_point
from django.conf import settings
from authentication.models import User
from client_management.models import AddClient
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
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    trip_type=models.CharField(max_length=50, null=True ,blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    currunt_location = gis_point.PointField(srid=453, null=True, blank=True)
    car_type=models.CharField(max_length=100, null=True)
    gear_type= models.CharField(max_length=100, null=True)
    pickup_location=models.CharField(max_length=100, null=True)
    drop_location=models.CharField(max_length=100, null=True)
    booking_time=models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.trip_type
    

# @receiver(post_save, sender=PlaceBooking)
# def create_booking(sender, instance, created, **kwargs):
#     if created:
#         PlaceBooking.objects.create(user=instance)

# @receiver(post_save, sender=PlaceBooking)
# def save_booking(sender, instance, **kwargs):
#     instance.Placebooking.save()


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
    
    






