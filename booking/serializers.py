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
from collections import OrderedDict
from django.contrib.gis.measure import D
from collections import OrderedDict

class ClientregistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = bookinguser
        fields = ['full_name', 'mobile_number', 'city', 'address']

        
class PlacebookingSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False)
    # add_driver = serializers.PrimaryKeyRelatedField(queryset=AddDriver.objects.all(), many=False, read_only=False)
    class Meta:
        model = PlaceBooking
        
        fields= ('id','trip_type', 'booking_date','no_of_days', 
                   'car_type', 'gear_type', 
                  'pickup_location', 'client_booking_time', 'drop_location', 'booking_time', 'currant_location', 'status','packege', 'mobile', 'user_address', 'deuty_started')
   

   
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
    #driver_name=serializers.SerializerMethodField()
    # booking_created_by=NewUserSerializer()
    class Meta:
        #driver_name=serializers.SerializerMethodField()
        #driver_name1 = MyDriverSerializer()
        model= AgentBooking
        fields= "__all__"

    # def get_driver_name(self, obj):
    #     #driver_name=obj.driver_name
    #     driver_name = obj.get('driver_name')
    #     add_driver_seri=MyDriverSerializer(driver_name)
    #     return add_driver_seri.data


    def to_representation(self, instance):
        data = super(Agentbookingserailizer, self).to_representation(instance)
        driver_name_data = data.get('driver_name')

        if isinstance(driver_name_data, dict):
        # If it's already a serialized dictionary, use it directly
            data['driver_name'] = driver_name_data
        elif isinstance(driver_name_data, int):
        # Handle the case where driver_name_data is an integer
            data['driver_name'] = {'driver_id': driver_name_data}
        elif driver_name_data is not None:
        # If it's a model instance, serialize it
         driver_data = MyDriverSerializer(driver_name_data).data
         data['driver_name'] = driver_data

        return data


# class Agentbookingserailizer(serializers.ModelSerializer):
#     #driver_name=serializers.SerializerMethodField()
#     # booking_created_by=NewUserSerializer()
#     class Meta:
#         driver_name=serializers.SerializerMethodField()
#         driver_name1 = MyDriverSerializer()
#         model= AgentBooking
#         fields= "__all__"

#     def get_driver_name(self, obj):
#         driver_name=obj.driver_name
#         add_driver_seri=MyDriverSerializer(driver_name)
#         return add_driver_seri.data
    
#     def to_representation(self, instance):
#         data = super(Agentbookingserailizer, self).to_representation(instance)
#         driver_data = MyDriverSerializer(instance.driver_name).data
#         data.update({
#             'driver_name': driver_data
#         })
#         return data
    
   
class BookLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLater
        fields = ['id','trip_type', 'from_date',
                  'to_date', 'car_type', 'gear_type', 'pickup_location', 'drop_location', 'booking_time', 'currant_location', 'status','packege', 'mobile', 'accepted_driver', "schedule_booking"]
        
class Userprofileserializer(serializers.ModelSerializer):
    model= userProfile
    fields='__all__'


class GuestBookingserialzer(serializers.ModelSerializer):
    class Meta:
        model=GuestBooking
        fields="__all__"