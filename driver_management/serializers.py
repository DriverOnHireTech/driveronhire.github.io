from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from user_master.serializers import *


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
    class Meta:
        model = AddDriver
        fields = "__all__"


class DriverleaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Driverleave
        fields=('drivername', 'reason', 'leave_from_date', 'leave_to_date', 'total_days_of_leave')
