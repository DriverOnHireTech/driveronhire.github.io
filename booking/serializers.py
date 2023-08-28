from rest_framework import serializers
from .models import  *
from driver_management.models import AddDriver
from driver_management.serializers import MyDriverSerializer
from user_master.models import Zone
from .models import bookinguser, Invoice

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from driver_management.models import Driverlocation
#from authentication.models import User
import json
from authentication.models import  User
from rest_framework_gis.serializers import GeometryField

class ClientregistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = bookinguser
        fields = ['full_name', 'mobile_number', 'city', 'address']

class PlacebookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False)
    drivers = serializers.SerializerMethodField()
    # current_location = GeometryField()
    # current
    class Meta:
        model = PlaceBooking
        fields= ['user','trip_type','current_location'
                 , 'car_type','drivers', 'gear_type', 'pickup_location', 'drop_location'
                 , 'booking_time']


    user= serializers.SerializerMethodField()
    

    def get_drivers(self,obj): 
        # you will replace driverlocation with firebase when you work with him   
        current_location = obj.current_location or None # this will be get from GIS
        if current_location is None:
            return None
        drivers = Driverlocation.objects.all().annotate(
            distance=Distance('driverlocation', # need to replace this by the drivers current location 
                Point(current_location.coords[0],
            current_location.coords[0],srid=current_location.srid))
            ).filter(distance__lt=D(km=1000))
        if not drivers.exists():
            return {
                "not found"
            }
        return drivers.values("driver")
# 15.3802703,44.2573765
        # return drivers.values("id","username")
    # return {
    #         "dj":'d'
    #     }
    def get_user(self, obj):
        return {
            "user":obj.user.username
        }
   

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddDriver
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    driver =  serializers.SerializerMethodField()
    placebooking = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ('user', 'driver','placebooking', 'add_favourite')
    def get_user(self, obj):
        user =  obj.user
        user_seri = ClientregistrationSerializer(user)
        print(user_seri)
        return user_seri.data
        
    def get_driver(self, obj):
        driver =  obj.driver
        print(driver)
        driver_seri = MyDriverSerializer(driver)
        return driver_seri.data
    
    def get_placebooking(self, obj):
        placebooking =  obj.placebooking
        driver_seri = PlacebookingSerializer(placebooking)
        return driver_seri.data


class Feedbackserializer(serializers.ModelSerializer):
    user =  serializers.SerializerMethodField()
    class Meta:

        model =  Feedback
        fields = "__all__"
   

