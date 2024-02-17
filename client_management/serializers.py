from rest_framework import serializers
from .models import *
from driver_management.serializers import MyDriverSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    addfavoritedriver_details = MyDriverSerializer(many=True, source='addfavoritedriver')
    class Meta:
        model=UserProfile
        fields=('user','user_name', 'usercar', 'useraddress', 'cartype', 'mobile_number','addfavoritedriver', 'addfavoritedriver_details')
        