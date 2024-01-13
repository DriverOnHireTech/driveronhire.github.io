from django.contrib.auth.models import User
from rest_framework import serializers, fields
from .models import *
from user_master.serializers import *
from authentication.serializers import NewUserSerializer


class BasicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicDetail
        fields = '__all__'


class DriversignupSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= '__all__'


class Driverlocationserializer(serializers.ModelSerializer):
    class Meta:
        model= Driverlocation
        fields= '__all__'


class MyDriverSerializer(serializers.ModelSerializer):
    # transmission_type = serializers.MultipleChoiceField(choices=transmission_option)
    # car_type = serializers.MultipleChoiceField(choices=car_option)
    first_name=serializers.CharField()
    class Meta:
        model = AddDriver
        fields = ["id","first_name", "sex", "mobile", "driver_type", "driving_licence", "driverlocation", 
                  "driver_update_date", "licence_no","pan_card_no","licence_type", "date_of_birth", "driver_status", "total_exp", "image_upload"]
  

class DriverleaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Driverleave
        fields=('reason', 'leave_from_date', 'leave_to_date', 'status')


class DriverReferserializer(serializers.ModelSerializer):
    class Meta:
        model = ReferDriver
        fields= ('name', 'mobile', 'location', 'branch')

class Driverappstatusserializer(serializers.ModelSerializer):
    # drivername= serializers.PrimaryKeyRelatedField(queryset=AddDriver.objects.all(),
    #                                               many=False) 
    class Meta:
        model= Driverappstatus
        fields="__all__"