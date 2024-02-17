from rest_framework import serializers
from .models import  *
from driver_management.models import AddDriver
from driver_management.models import Driverlocation
from driver_management.serializers import MyDriverSerializer
from user_master.models import Zone
from .models import bookinguser, BookLater
from authentication.serializers import NewUserSerializer

from authentication.models import  User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from collections import OrderedDict
from django.contrib.gis.measure import D
from collections import OrderedDict
# from user_master.models import ZoneA, ZoneB, ZoneC, ZoneD, ZoneE, ZoneF, ZoneG

from user_master.models import *

class ClientregistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = bookinguser
        fields = ['full_name', 'mobile_number', 'city', 'address']

        
class PlacebookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceBooking
        
        fields= ('id','trip_type','booking_date','no_of_days', 'booking_type', 
                   'car_type', 'gear_type', 
                  'pickup_location', 'client_booking_time', 'drop_location', 'booking_time', 'deuty_started','journy_started',
                  'journy_started','currant_location', 'status','packege',  'user_address','cancelbooking_reason', 'cancelbooking_message', 'mobile', 'accepted_driver_name', 'accepted_driver_number')
        
   
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
    
    # driver =  serializers.SerializerMethodField()
    placebooking = serializers.SerializerMethodField()
    driver=serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = "__all__"

  
    
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

    class Meta:
        # driver_name=serializers.SerializerMethodField()
        driver_name = MyDriverSerializer()
        model= AgentBooking
        fields= "__all__"


    
    def to_representation(self, instance):
        data = super(Agentbookingserailizer, self).to_representation(instance)
        print("Data: ",data)
        data['id'] = instance.id

        if 'driver_name' in data:
            driver_instance = instance.driver_name
            if driver_instance:
                driver_data = MyDriverSerializer(driver_instance).data
                data['driver_name'] = driver_data
            else:
                data['driver_name'] = None
        

        #  Get the name from the related user model
            # data.update({
            #     'driver_name': driver_data,
            # })
        return data
    
   
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

class place_agent_booking_serializer(serializers.Serializer):
    table1_data = PlacebookingSerializer(many=True)
    table2_data = Agentbookingserailizer(many=True)


class ZoneASerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneA
        fields = "__all__"

    
class ZoneBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneB
        fields = "__all__"


class ZoneCSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneC
        fields = "__all__"


class ZoneDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneD
        fields = "__all__"


class ZoneESerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneE
        fields = "__all__"


class ZoneFSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneF
        fields = "__all__"


class ZoneGSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoneG
        fields = "__all__"

class DeclinebookingSerializer(serializers.ModelSerializer):
    placebooking=serializers.SerializerMethodField()
    agentbooking=serializers.SerializerMethodField()
    class Meta:
        model=Declinebooking
        fields= '__all__'
    
    def get_placebooking(self,obj):
        placebooking =  obj.placebooking
        driver_seri = PlacebookingSerializer(placebooking)
        return driver_seri.data
    
    def get_agentbooking(self, obj):
        agentbooking=obj.agentbooking
        agnetseri=Agentbookingserailizer(agentbooking)
        return agnetseri.data

#Pune location models and serializer
class punelocationASerializer(serializers.ModelSerializer):
    class Meta:
        model=pune_A_location
        fields= '__all__'

class punelocationBSerializer(serializers.ModelSerializer):
    class Meta:
        model=pune_B_location
        fields= '__all__'
