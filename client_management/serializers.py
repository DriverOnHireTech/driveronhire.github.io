from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=('user_name', 'usercar', 'useraddress', 'cartype', 'mobile_number')
        