from django.db import models
from django.conf import settings
from booking.models import PlaceBooking, AgentBooking
from driver_management.models import AddDriver
from user_master.models import *

class AddClient(models.Model):
    client_name = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=13)
    alternate_number = models.CharField(max_length=13, null=True, blank=True)
    email_id = models.EmailField()
    reference = models.CharField(choices=(("1", "google"), ("2", "Facebook"), ("3", "Website"),
                                          ("4", "Previous Client"), ("5", "Other")),
                                 max_length=10)

    def __str__(self):
        return self.client_name
#
# user car
class UserCar(models.Model):
    user_car=models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user_car

class Address(models.Model):
    address1 = models.CharField(max_length=20, null=True, blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_address", null=True,blank=True)
    #state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    #city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    #location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

# User Profile

class UserProfile(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user", null=True,blank=True)
    addfavoritedriver=models.ManyToManyField(AddDriver,null=True, blank=True)
    user_name=models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=50, null=True, blank=True)
    usercar=models.CharField(max_length=200, null=True, blank=True)
    cartype=models.CharField(max_length=200, null=True, blank=True)
    useraddress1=models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    addprofile=models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.user_name
