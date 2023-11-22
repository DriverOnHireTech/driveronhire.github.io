from rest_framework import serializers
from .models import  *
from driver_management.models import AddDriver
from driver_management.models import Driverlocation
from driver_management.serializers import MyDriverSerializer
from user_master.models import Zone
from .models import bookinguser, Invoice, BookLater
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
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False)
    # add_driver = serializers.PrimaryKeyRelatedField(queryset=AddDriver.objects.all(), many=False, read_only=False)

    # drivers = serializers.SerializerMethodField()
    class Meta:
        model = PlaceBooking
        
        fields= ('id','trip_type', 'booking_date','no_of_days',
                   'car_type', 'gear_type', 
                  'pickup_location', 'client_booking_time', 'drop_location', 'booking_time', 'currant_location', 'status','packege', 'mobile')

    # def get_user(self, obj):
    #     user =  obj.driver
    #     user_seri = MyDriverSerializer(user)
    #     return user_seri.data

   
class NotifyDriverSerializer(serializers.ModelSerializer):
    place_booking_id = serializers.SerializerMethodField()

    class Meta:
        model = Notifydrivers
        fields = "__all__"

    def get_place_booking_id(self, obj):
        place_booking = obj.place_booking
        return place_booking.id if place_booking else None
    

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddDriver
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    
    driver =  serializers.SerializerMethodField()
    placebooking = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ('driver','placebooking', 'add_favourite')

  
    
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
    


class Agentbookingserailizer(serializers.ModelSerializer):
    driver_name=serializers.SerializerMethodField()
    class Meta:
        driver_name=serializers.SerializerMethodField()
        driver_name1 = MyDriverSerializer()
        model= AgentBooking
        fields= "__all__"

    def get_driver_name(self,obj):
        driver_name=obj.driver_name
        adddriver_seri= MyDriverSerializer(driver_name)
        return adddriver_seri.data
    
    def to_representation(self, instance):
        data = super(Agentbookingserailizer, self).to_representation(instance)
        driver_data = MyDriverSerializer(instance.driver_name).data
        data.update({
            'driver_name': driver_data
        })
        print("data updated: ", data)
        return data
    
   
class BookLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLater
        fields = ['id','trip_type', 'from_date',
                  'to_date', 'car_type', 'gear_type', 'pickup_location', 'drop_location', 'booking_time', 'currant_location', 'status','packege', 'mobile', 'accepted_driver', "schedule_booking"]
        
class Userprofileserializer(serializers.ModelSerializer):
    model= userProfile
    field='__all__'