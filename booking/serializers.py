from rest_framework import serializers
from .models import  *
from driver_management.models import AddDriver
from driver_management.serializers import MyDriverSerializer
from user_master.models import Zone
from .models import bookinguser, Invoice
from authentication.serializers import NewUserSerializer

from authentication.models import  User

class ClientregistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = bookinguser
        fields = ['full_name', 'mobile_number', 'city', 'address']

        
class PlacebookingSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, read_only=False)
    user = NewUserSerializer()
    class Meta:
        model = PlaceBooking
        
        fields= ['id','user','trip_type', 'from_date', 'to_date', 'car_type', 'gear_type', 'pickup_location', 'drop_location', 'booking_time', 'currunt_location']


    user= serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.phone



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


   

