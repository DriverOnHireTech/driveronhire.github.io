from rest_framework import serializers
from .models import  *
from driver_management.models import AddDriver
from driver_management.models import Driverlocation
from driver_management.serializers import MyDriverSerializer
from user_master.models import Zone
from .models import bookinguser, Invoice
from authentication.serializers import NewUserSerializer

from authentication.models import  User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

class ClientregistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = bookinguser
        fields = ['full_name', 'mobile_number', 'city', 'address']

        
class PlacebookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False)
    
    drivers = serializers.SerializerMethodField()
    class Meta:
        model = PlaceBooking
        
        fields= ['id','user','trip_type', 'from_date', 'to_date', 'car_type', 'gear_type', 'pickup_location', 'drop_location', 'booking_time', 'currant_location', 'status', 'accepted_driver', 'drivers']

  
    def create(self, validated_data):
        current_location_dict = validated_data.pop('currant_location')  # Fixed the typo here
        longitude = current_location_dict["coordinates"][0]
        latitude = current_location_dict["coordinates"][1]
        print("lLongitude\n: latitude:", longitude,latitude )
        currant_location = Point(longitude, latitude, srid=4326)  # Corrected the variable name here
        validated_data['currant_location'] = currant_location
        return super().create(validated_data)

    def get_drivers(self, obj):
        currant_location = obj.currant_location or None
        if currant_location is None:
            return None
        driver =Driverlocation.objects.all().annotate(
              distance = Distance('driverlocation', currant_location)
              ).filter(distance__lte=D(km=3))
        
                     
        if not driver.exists():
            return {"not found"}
        return driver.values("driver")
    
    def get_user(self, obj):
        return {'user':obj.user.username}
    

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
        return user_seri.data
    
    def get_driver(self, obj):
        driver =  obj.driver
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
    

class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


   

