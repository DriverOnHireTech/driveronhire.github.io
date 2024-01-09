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
from user_master.models import ZoneA, ZoneB, ZoneC, ZoneD, ZoneE, ZoneF, ZoneG

class ClientregistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = bookinguser
        fields = ['full_name', 'mobile_number', 'city', 'address']

        
class PlacebookingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.phone 
        
    class Meta:
        model = PlaceBooking
        
        fields= ('id','user','trip_type', 'booking_date','no_of_days', 
                   'car_type', 'gear_type', 'mobile', 
                  'pickup_location', 'client_booking_time', 'drop_location', 'booking_time', 'deuty_started','currant_location', 'status','packege',  'user_address','cancelbooking_reason', 'cancelbooking_message')
   
   
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
    # placebooking = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = ('driver','placebooking', 'add_favourite')

  
    
    # def get_driver(self, obj):
    #     driver =  obj.driver
    #     driver_seri = MyDriverSerializer(driver)
    #     return driver_seri.data
    
    # def get_placebooking(self, obj):
    #     placebooking =  obj.placebooking
    #     driver_seri = PlacebookingSerializer(placebooking)
    #     return driver_seri.data


class Feedbackserializer(serializers.ModelSerializer):
    user =  serializers.SerializerMethodField()
    class Meta:
        model =  Feedback
        fields = "__all__"
    

# class Agentbookingserailizer(serializers.ModelSerializer):
#     #driver_name=serializers.SerializerMethodField()
#     # booking_created_by=NewUserSerializer()
#     class Meta:
#         #driver_name=serializers.SerializerMethodField()
#         #driver_name1 = MyDriverSerializer()
#         model= AgentBooking
#         fields= "__all__"

#     # def get_driver_name(self, obj):
#     #     #driver_name=obj.driver_name
#     #     driver_name = obj.get('driver_name')
#     #     add_driver_seri=MyDriverSerializer(driver_name)
#     #     return add_driver_seri.data


#     def to_representation(self, instance):
#         data = super(Agentbookingserailizer, self).to_representation(instance)
#         print("Data value: ", data)
#         driver_name_data = data.get('driver_name')
#         print("driver name: ", driver_name_data)

#         if isinstance(driver_name_data, dict):
#             # If it's already a serialized dictionary, use it directly
#             data['driver_name'] = driver_name_data
#         elif driver_name_data is not None:
#             # If it's a model instance, serialize it
#             driver_data = MyDriverSerializer(driver_name_data).data
#             print("driver data: ", driver_data)
#             data['driver_name'] = driver_data

#         return data


class Agentbookingserailizer(serializers.ModelSerializer):

    class Meta:
        # driver_name=serializers.SerializerMethodField()
        driver_name = MyDriverSerializer()
        model= AgentBooking
        fields= "__all__"


    # def get_driver_name(self, obj):
    #     driver_name=obj.driver_name
    #     add_driver_seri=MyDriverSerializer(driver_name)
    #     return add_driver_seri.data
    
    def to_representation(self, instance):
        data = super(Agentbookingserailizer, self).to_representation(instance)
        data['id'] = instance.id

        if 'driver_name' in data:
            driver_instance = instance.driver_name
            if driver_instance:
                driver_data = MyDriverSerializer(driver_instance).data
                data['driver_name'] = driver_data
            else:
                data['driver_name'] = None
        

         # Get the name from the related user model
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